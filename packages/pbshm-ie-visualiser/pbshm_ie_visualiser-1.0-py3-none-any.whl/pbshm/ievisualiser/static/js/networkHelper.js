import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import { LineGeometry } from 'three/addons/lines/LineGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { Line2 } from 'three/addons/lines/Line2.js';

import * as gui from './guiHelper.js';
import { extractRelationships } from './jsonHelper.js';
import * as colours from './colourHelper.js';


/**
 * Create an attributed graph of a model from the json file.
 * @param {string} rawtext Raw json formatted string
 */
function plotNetworkFromFile(rawtext){
    // Get information on network edges
    const data = JSON.parse(rawtext);
    const elements = data.models.irreducibleElement.elements;
    const relat  = data.models.irreducibleElement.relationships;
    const nElements = elements.length;
    // Store the edges in both directions of the bi-directional graph
    // edgeCoords is used when we know the locations of where two elements are connected (but not the location of the element)
    // so we can use this information to draw the nodes of the graph in roughly the correct area that they appear in the structure.
    let edgeCoords = [...Array(nElements)].map(e => Array()); 
    let edges = [...Array(nElements)].map(e => Array());  // which other nodes each node is connected too
    let elInfo = [];  // i.e. context, material, etc.
    let elNames = [];
    // Keep a count of how many edges each node has
    let counts = new Array(nElements); for (let i=0; i<nElements; ++i) counts[i] = 0;
    elements.forEach((node) => {
        elNames.push(node.name);
    });
    let nodej, nodek, i, j, k, x, y, z;
    for (i=0; i<relat.length; i++){
        for (j=0; j<relat[i].elements.length-1; j++){
            nodej = elNames.indexOf(relat[i].elements[j].name);
            for (k=1; k<relat[i].elements.length; k++){
                nodek = elNames.indexOf(relat[i].elements[k].name);
                edges[nodej].push(nodek);
                edges[nodek].push(nodej);
                counts[nodej]++;
                counts[nodek]++;
            }
        }
        if ("coordinates" in relat[0].elements[1]){
            x = relat[i].elements[0].coordinates.global.translational.x.value;
            y = relat[i].elements[0].coordinates.global.translational.y.value;
            z = relat[i].elements[0].coordinates.global.translational.z.value;
            edgeCoords[nodej].push([x, y, z])
            edgeCoords[nodek].push([x, y, z])
        }
    }
    
    // Get natures of relationships and unpack groups of more than two in a connection
    // to just the paired natures.
    const [relationships, natures] = extractRelationships(rawtext);
    let naturePairs = [];
    const keys = Object.keys(natures)
    for (i=0; i<keys.length; i++){
        const groupedElNames = keys[i].split(',');
        for (j=0; j<groupedElNames.length-1; j++){
            for (k=1; k<groupedElNames.length; k++){
                naturePairs[[groupedElNames[j], groupedElNames[k]]] = natures[keys[i]];
            }
        }
    }

    // Get information on context, material, etc for each element.
    for (i=0; i<elNames.length; i++){
        try {
            elInfo[i] = elements[i]
        } catch {;}  // no material type given
    }
    // See if there were any coordinates given detailing where two elements join.
    let totalCoords = 0;
    for (i=0; i<edgeCoords.length; i++){
        totalCoords += edgeCoords[i].length;
    }
    let nodeCoords;
    // If none were given then calculate where to position the nodes.
    if (totalCoords == 0){
        nodeCoords = fruchterman_reingold(edges);
        drawNetwork(nodeCoords, edges, elInfo, naturePairs, true)
    }
    // If joint coordinates were given then use them to decide on node coordinates.
    else{
        let tempEdges = edges.map(function(arr) {
            return arr.slice();
        });
        nodeCoords = getNodeCoords(tempEdges, edgeCoords, counts);
        drawNetwork(nodeCoords, edges, elInfo, naturePairs);
    }
}

/**
 * Given edgeCoords (where two elements are joined),
 * decide what the coordinates of the nodes should be.
 *   
 * This method takes the least popular node and uses the coordinates of
 * its first known joint with another element to decide where to place the node.
 * It then cycles through, looking at the next least popular node, until all have been considered.
 * @param {int[int[]]} edges 2D array listing all node edges
 * @param {int[int[]]} edgeCoords 2D array listing the coordinates where elements are connected in the real structure
 * @param {int[]} counts 1D array listing how many edges each node has
 * @returns Array of [x, y, z] coordinates for each node.
 */
function getNodeCoords(edges, edgeCoords, counts){
    let e1, e2;
    const nElements = edges.length;
    let nodeCoords = [...Array(nElements)].map(e => [0, 0, 0]);
    let minCount = Math.min(...counts)
    while (minCount < Infinity){
        e1 = counts.indexOf(minCount);
        e2 = edges[e1][0];
        // remove the used edge
        edges[e1].shift();  // used first edge of e1
        edges[e2].splice(edges[e2].indexOf(e1), 1);  // find and remove e1 edge in e2
        nodeCoords[e1] = edgeCoords[e1][0];
        counts[e1] -= 1;  // so it doesn't get called again
        counts[e2] -= 1;
        if (counts[e1] == 0){ counts[e1] = Infinity; }
        if (counts[e2] == 0){ counts[e2] = Infinity; }
        minCount = Math.min(...counts)
    }
    return nodeCoords;
}


/**
 * Render the network graph using threejs.
 * @param {int[int[]]} coords Array of [x,y,z] coordinates for each node.
 * @param {int[int[]]} edges 2D array listing all node edges
 * @param {dict} elInfo Information relating to each node
 * @param {string[]} natures Array of relationship nature types of each edge
 * @param {boolean} threeD Plot the model as three-dimensional (default) or two-dimensional
 */
function drawNetwork(coords, edges, elInfo, natures, threeD=true){
    const nNodes = coords.length;
    let minX = 0;
    let minY = 0
    let maxX = 0;
    let maxY = 0;
    let maxZ = 0;
    coords.forEach((node) => {
        minX = Math.min(minX, node[0]);
        minY = Math.min(minY, node[1]);
        maxX = Math.max(maxX, node[0]);
        maxY = Math.max(maxY, node[1]);
        maxZ = Math.max(maxZ, node[2]);
    });

    // Scale coords to fit on the canvas
    // The canvas is (300 * 150) but scale to (200 * 100) so the nodes aren't right on the edge
    for (let i=0; i<coords.length; i++){
        const x = coords[i][0]
        const y = coords[i][1]
        coords[i][0] = ((x - minX) / (maxX - minX)) * 200 - 100
        coords[i][1] = ((y - minY) / (maxY - minY)) * 100 - 50
    }

    const canvas = document.querySelector('#c');
    const renderer = new THREE.WebGLRenderer({antialias: true, canvas});
    const scene = new THREE.Scene();
    scene.background = new THREE.Color( 'white' );
    let camera;
    if (threeD){
        const fov = 30;	 // field of view - determines width of near and far planes
        const aspect = 2;  // the canvas default (300 x 150)
        const near = 1;	 // height of near plane
        const far = 500;  // height of far plane
        camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
        camera.position.set(0, 0, Math.min(300));  // where the camera is located
    }
    else{
        camera = new THREE.OrthographicCamera(-150, 150, 75, -75, -1, 1);
        camera.zoom = 1;
    }

    renderer.render( scene, camera );
    // Give the user the ability to control the camera
    const controls = new OrbitControls(camera, canvas);
    controls.target.set(0, 0, 0);	// where the camera looks
    controls.update();

    // GUI for changing the colour scheme
	colours.addColourFolders(gui.coloursFolder, render, "contextual", true);
	gui.setViewerMode();
  
    const intensity = 3;
    const light = new THREE.AmbientLight(0xFFFFFF, intensity);
    scene.add(light);
    
    // Plot the nodes
    for (let i=0; i<nNodes; i++){
        const shape = makeInstance(new THREE.SphereGeometry(2, 12, 8),
                                    coords[i][0],
                                    coords[i][1],
                                    coords[i][2],
                                    elInfo[i]);
        colours.cElements.push(shape);
        if (shape.el_contextual != "ground") {
			colours.makeContextColourVisible(shape.el_contextual);
			colours.makeMaterialColourVisible(shape.el_material);
			colours.makeGeometryColourVisible(shape.el_geometry);
		}
    }
    
    // Plot the edges
    let pos1, pos2;
    for (let i=0; i<nNodes; i++){
        pos1 = coords[i];
        for (let j=0; j<edges[i].length; j++){
            if (i < edges[i][j]) {  // don't draw lines twice (once for each way)
                pos2 = coords[edges[i][j]];
                const nature = currentRelationshipNature(elInfo[i].name, elInfo[edges[i][j]].name);
                colours.makeEdgeColourVisible(nature);
                drawLine(pos1, pos2, nature);
            }
        }
    }

    document.addEventListener('pointerdown', selectElement);

    /**
     * If a node is selected by the user, set the gui to show the information.
     * @param {event} event pointerDown event
     */
	function selectElement(event){
		let raycaster = new THREE.Raycaster();
		let pointer = new THREE.Vector2();
		pointer.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 );
		raycaster.setFromCamera( pointer, camera );
		const intersects = raycaster.intersectObjects( colours.cElements, false );
		if ( intersects.length > 0 ) {
            const currentObject = intersects[0].object;
            gui.setGeometryFolder(currentObject);
            gui.gCoordsFolder.hide();
            gui.sphereFolder.hide();
		}
	}

    /**
     * Find out the relationship nature of the two elements
     * @param {int} id1 Index of element 1 within the 2D array of edges
     * @param {int} id2 Index of element 2
     * @returns Relationship nature as string
     */
    function currentRelationshipNature(id1, id2){
        if (natures[[id1, id2]] != undefined){
            return natures[[id1, id2]];
        } else if (natures[[id2, id1]] != undefined){
            return natures[[id2, id1]];
        }
    }

    /**
     * Render the threejs elements.
     */
    function render() {
      if ( resizeRendererToDisplaySize( renderer ) ) {
        const canvas = renderer.domElement;
        camera.aspect = canvas.clientWidth / canvas.clientHeight;
        camera.updateProjectionMatrix();
      }
      renderer.render( scene, camera );
      requestAnimationFrame( render );
    }

    /**
     * Check if the threejs elements need to be updated because the screen is resized (avoids distortion).
     * @param {THREE.render} renderer 
     * @returns boolean
     */
    function resizeRendererToDisplaySize( renderer ) {
        const canvas = renderer.domElement;
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;
        const needResize = canvas.width !== width || canvas.height !== height;
        if ( needResize ) {
            renderer.setSize( width, height, false );
        }
        return needResize;
    }
    
    /**
     * Add a shape to the threejs scene.
     * @param {THREE.geometry} geometry 
     * @param {float} x coordinate
     * @param {float} y coordinate
     * @param {float} z coordinate
     * @param {dict} info information of the element (e.g. material, contextual type, etc.)
     * @returns THREE.mesh object of the node that has been added to the scene
     */
    function makeInstance(geometry, x, y, z, info) {
        let element_type;
        let element_material;
        let element_geom;
        if (info.type != "ground") {
            element_type = info.contextual.type;
            // Material and geometry may have two or three bits of information
            try {
                element_material = [info.material.type.name, info.material.type.type.name, info.material.type.type.type.name].join("-");
            } catch(TypeError) {
                try {
                    element_material = [info.material.type.name, info.material.type.type.name].join("-");
                } catch(TypeError) {
                    element_material = info.material.type.name;
                }
            }
            try {
                element_geom = [info.geometry.type.name, info.geometry.type.type.name, info.geometry.type.type.type.name].join(" ");
            } catch(TypeError) {
                element_geom = [info.geometry.type.name, info.geometry.type.type.name].join(" ");
            }
        } else {
            element_type = "ground";
        }
        let colour;
        if (element_type == "ground"){
            colour = colours.otherColours["ground"];
        } else {
            colour = colours.contextualColours[element_type];  // contextual is the default colour scheme on load
        }
        const material = new THREE.MeshPhongMaterial({color: colour});
        const shape = new THREE.Mesh(geometry, material);
        shape.name = info['name'];
        shape.full_info = info;
        shape.el_material = element_material;
        shape.el_contextual = element_type;
        shape.el_geometry = element_geom;
        shape.position.x = x;
        shape.position.y = y;
        shape.position.z = z;
        scene.add(shape);
        return shape;
    }
    
    /**
     * Draw the network edge between two nodes
     * @param {[float, float, float]} pos1 [x,y,z] of one end of the edge
     * @param {[float, float, float]} pos2 [x,y,z] of the other end of the edge
     * @param {string} nature relationship nature type of the connection
     */
    function drawLine(pos1, pos2, nature){
      const geometry = new LineGeometry();
      geometry.setPositions([pos1[0], pos1[1], pos1[2], pos2[0], pos2[1], pos2[2]]);
      const edge = new Line2( geometry, new LineMaterial( {color: colours.relationshipColours[nature], linewidth: 0.002 } ) )
      edge.nature = nature;
      colours.cLines.push(edge);
      scene.add(edge);
    }
    
    requestAnimationFrame(render);
}

/**
 * Decide on the coordinates of the nodes given a list of edges.
 * Edges is a list of lists. Each row is a node and each element in a
 * row lists the indexes of the edges shared with the node.
 * Uses the method in
 *     Fruchterman, Thomas MJ, and Edward M. Reingold.
 *     "Graph drawing by force‐directed placement."
 *     Software: Practice and experience 21, no. 11 (1991): 1129-1164.
 * @param {*} edges 2D array listing all node edges
 * @param {int} iterations Total iterations with which to loop the process
 * @returns A list of [x,y] coordinates for each node
 */
function fruchterman_reingold(edges, iterations=50){
    /**
     * Create a two-dimensional array and fill each index with the same value
     * @param {int} w width
     * @param {int} h height
     * @param {*} val value
     * @returns 
     */
    function makeArray(w, h, val) {
        var arr = [];
        for(let i = 0; i < h; i++) {
            arr[i] = [];
            for(let j = 0; j < w; j++) {
                arr[i][j] = val;
            }
        }
        return arr;
    }
	const dimens = 3;
	const nVertices = edges.length;
	const k = Math.sqrt(1 / nVertices);  // Optimal distance between nodes
	
	// Create the adjacency matrix
	let A = makeArray(nVertices, nVertices, 0);
	let i;
	for (i=0; i<nVertices; i++){
		for (const e of edges[i]){
			A[i][e] = 1;
			A[e][i] = 1;
		}
	}

	// Create random initial positions
	let pos = [];
	for (let i = 0; i < nVertices; i++) {
        pos[i] = [];
        for (let j = 0; j < dimens; j++) {
			pos[i][j] = Math.random();
        }
    }
	
	// Set initial temperature
	const arrayColumn = (arr, n) => arr.map(x => x[n]);
	let t = Math.max((Math.max.apply(Math, arrayColumn(pos, 0)) - Math.min.apply(Math, arrayColumn(pos, 0))),
	                 (Math.max.apply(Math, arrayColumn(pos, 1)) - Math.min.apply(Math, arrayColumn(pos, 1))));
	const dt = t / (iterations + 1);

	let displacement = makeArray(dimens, nVertices, 0);
	let delta, dist, dx, dy;
	let length, delta_pos;
	for (let iter=0; iter<iterations; iter++){
		// reset displacement
		for (let i = 0; i < nVertices; i++) {
			for (let j = 0; j < dimens; j++) {
				displacement[i][j] = 0;
			}
		}
		for (i=0; i<nVertices; i++){
			// Get the euclidean distance between this node's position and all others
			delta = makeArray(2, nVertices, 0);
			dist = [];
			for (let j=0; j<nVertices; j++){
				delta[j][0] = pos[i][0] - pos[j][0];
				delta[j][1] = pos[i][1] - pos[j][1];
				dist[j] = Math.sqrt(delta[j][0]**2 + delta[j][1]**2);
				// Enforce minimum distance of 0.01
				if (dist[j] < 0.01){
					dist[j] = 0.01;
				}
			}
			// Get the displacement force and sum for each separate axis
			dx = 0;
			dy = 0;
			for (let j=0; j<nVertices; j++){
				dx += delta[j][0] * (k * k / dist[j]**2 - A[i][j] * dist[j] / k)
				dy += delta[j][1] * (k * k / dist[j]**2 - A[i][j] * dist[j] / k)
			}
			displacement[i][0] = dx;
			displacement[i][1] = dy;
		}
		
		// Update positions
		for (i=0; i<nVertices; i++){
			length = Math.sqrt(displacement[i][0]**2 + displacement[i][1]**2);
			if (length < 0.01){
				length = 0.01;
			}
			delta_pos = [displacement[i][0] * t / length, displacement[i][1] * t / length];
			pos[i][0] += delta_pos[0]
			pos[i][1] += delta_pos[1]
		}

		// Cool temperature
		t -= dt;
	}

	// Rescale
	let meanX = 0;
	let meanY = 0;
	for (i=0; i<nVertices; i++){
		meanX += pos[i][0];
		meanY += pos[i][1];
	}
	meanX /= nVertices;
	meanY /= nVertices;
	for (i=0; i<nVertices; i++){
		pos[i][0] -= meanX;
		pos[i][1] -= meanY;
	}
	
	return pos;
}

export {plotNetworkFromFile};