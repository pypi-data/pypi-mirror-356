import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

import { otherColours, contextualColours } from './colourHelper.js';
import { TrapezoidGeometry } from './trapezoid.js';
import {ObliqueCylinderGeometry} from './obliqueCylinder.js'
import { jsonToGl } from './translationHelper.js';


/**
 * Creates a threejs mesh object of the element.
 * @param {dict} element A dictionary of details about the element found in the json file.
 * @param {int} scaleFactor Amount by which to scale the geomtries down (useful for large structures that can look distorted when kept full size)
 * @returns THREE.mesh object of the element
 */
function geometryDetails(element, scaleFactor=1){
    let geometry;
    if (element["method"] == "translate" || element["method"] == "regular"){
        if (element["shape"] == "cuboid" || element["shape"] == "rectangular"){
            const width = element["dimensions"].length / scaleFactor;	// width in threejs but length in json
            const depth = element["dimensions"].width / scaleFactor;
            const height = element["dimensions"].height / scaleFactor;
            geometry = new THREE.BoxGeometry(width, height, depth);
        }
        else if (element["shape"] == "sphere") {
            const radius = element["dimensions"].radius;
            geometry = new THREE.SphereGeometry(radius);
        }
        else if (element["shape"] == "cylinder" || element["shape"] == "circular") {
            const radius = element["dimensions"].radius;
            const length = element["dimensions"].length;
            geometry = new THREE.CylinderGeometry(radius, radius, length);
            geometry.rotateZ(Math.PI/2);  // rotate because cylinder is horizontal in json but vertical in webGL
        }
        else if (element["shape"] == "i-beam" || element["shape"] == "c-beam"){
            const width = element["dimensions"].length / scaleFactor;
            const h = element["dimensions"].h / scaleFactor;
            const s = element["dimensions"].s / scaleFactor;
            const t = element["dimensions"].t / scaleFactor;
            const b = element["dimensions"].b / scaleFactor;
            geometry = generateBeam(element["shape"], width=4, h=4, s=1, t=1, b=1)
        }
        else if (element["shape"] == "other"){
            console.log("Element", element["element_name"], "is shape other.");
        }
    }
    else if (element["method"] == "translateAndScale"){
        if (element["shape"] == "cuboid"){
            const leftTransY = element["faces"].left.translational.y.value / scaleFactor;
            const leftTransZ = element["faces"].left.translational.z.value / scaleFactor;
            const leftDimensY = element["faces"].left.dimensions.y.value / scaleFactor;
            const leftDimensZ = element["faces"].left.dimensions.z.value / scaleFactor;
            const rightTransY = element["faces"].right.translational.y.value / scaleFactor;
            const rightTransZ = element["faces"].right.translational.z.value / scaleFactor;
            const rightDimensY = element["faces"].right.dimensions.y.value / scaleFactor;
            const rightDimensZ = element["faces"].right.dimensions.z.value / scaleFactor;
            const width = element["dimensions"].length / scaleFactor;	// called length in json
            geometry = new TrapezoidGeometry(leftTransY, leftTransZ,
                leftDimensY, leftDimensZ, rightTransY, rightTransZ,
                    rightDimensY, rightDimensZ, width);
        }
        else if (element["shape"] == "cylinder"){
            const width = element["dimensions"].length / scaleFactor;	// called length in json
            const leftTransY = element["faces"].left.translational.y.value / scaleFactor;
            const leftTransZ = element["faces"].left.translational.z.value / scaleFactor;
            const rightTransY = element["faces"].right.translational.y.value / scaleFactor;
            const rightTransZ = element["faces"].right.translational.z.value / scaleFactor;
            const leftRadius = element["faces"].left.dimensions.radius.value / scaleFactor;
            const rightRadius = element["faces"].left.dimensions.radius.value / scaleFactor;
            const skewY = rightTransY - leftTransY;
            const skewZ = -(rightTransZ - leftTransZ);  // z is in opposite direction in json to webGL
            geometry = new ObliqueCylinderGeometry(rightRadius, leftRadius, width, skewY, skewZ);
            // Rotate because cylinder is assumed horizontal in json but automatically vertical in webGL
            geometry.rotateZ(Math.PI/2);
        }
        else if (element["shape"] == "other"){
            console.log("Element", element["element_name"], "is shape other.");
        }
    }
    else {
        console.error("Unknown handling method", element["method"]);
    }
    let colour;
    if (element["element_type"] == "ground"){
        colour = otherColours;
    } else {
        colour = contextualColours[element["element_type"]];
    }
    const material = new THREE.MeshPhongMaterial({color: colour});
    const shape = new THREE.Mesh(geometry, material);
    shape.full_info = element["full_info"];
    shape.name = element["element_name"];
    shape.el_material = element["element_material"];
    shape.el_contextual = element["element_type"];
    if (element["element_geometry"] == undefined || element["element_geometry"].substring(0, 9) == "undefined") {
        shape.el_geometry = undefined;    
    } else {
        shape.el_geometry = element["element_geometry"];
        if (shape.el_geometry.substring(0, shape.el_geometry.indexOf(' ')) == 'shell'){
            shape.geometry.parameters["thickness"] = element["dimensions"].thickness;
        } else {
            shape.geometry.parameters["thickness"] = 1;  // default in case element is changed to shell
        }
    }
    // Threejs automatically puts a shape's (x,y,z) coords in the centre.
    // In json an element's (x,y,z) coords relate to its bottom, left, front corner.
    // Therefore each coordinate must be translated to the correct location.
    shape.position.x = jsonToGl(shape, 'x', element["coords"][0]);
    shape.position.y = jsonToGl(shape, 'y', element["coords"][1]);
    shape.position.z = jsonToGl(shape, 'z', element["coords"][2]);
    
    if (element["rotation"] != undefined){
        if (element["rotation"].alpha.unit == "radians"){
            shape.rotateX(element["rotation"].alpha);    
        }
        else{
            shape.rotateX(element["rotation"].alpha * (Math.PI/180));
        }

        if (element["rotation"].beta.unit == "radians"){
            shape.rotateY(element["rotation"].beta);    
        }
        else{
            shape.rotateY(element["rotation"].beta * (Math.PI/180));
        }
        // Note the sign change as positive z in json is negative z in webgl
        if (element["rotation"].gamma.unit == "radians"){
            shape.rotateZ(-element["rotation"].gamma);    
        }
        else{
            shape.rotateZ(-element["rotation"].gamma * (Math.PI/180));
        }
    }
    return shape;
}


/**
 * Create a threejs geometry for an i-beam or c-beam.
 * -> ---------------  <-
     t  |             |   |
     -> ------   ------   |
             |   |        |
             | s |        |h
             |   |        |
        ------   ------   |
        |             |   |
        ---------------  <-
                b
 * @param {string} type "i-beam" or "c-beam"
 * @param {int} width width of entire beam
 * @param {int} h height of entire beam
 * @param {int} s depth of centre section
 * @param {int} t height of top and bottom sections
 * @param {int} b depth of entire beam
 * @returns THREE.geometry
 */
function generateBeam(type, width=4, h=4, s=1, t=1, b=1){
    // Create three cuboids to represent the beam
    const bottomGeom = new THREE.BoxGeometry(width, t, b);
    const middleGeom = new THREE.BoxGeometry(width, h-(t*2), s);
    const topGeom = new THREE.BoxGeometry(width, t, b);

    // Translate the locations for each of the three parts of the i-beam
    // x and z locations are the same for each part (except c-beam)
    bottomGeom.translate(0, (t/2)-(h/2), 0);
    topGeom.translate(0, (h/2)-(t/2), 0);
    if (type == "c-beam"){
        middleGeom.translate(0, 0, (- b + s) / 2);
    }
    
    // A few methods exist in threejs for joining multiple geomtries into one.
    // mergegeometries is the only one that works effectively for correct translation and rotation in the builder.
    const geometry = mergeGeometries([bottomGeom, middleGeom, topGeom]);
    if (type == "c-beam"){
        geometry.type = "CBeamGeometry";
    } else {
        geometry.type = "IBeamGeometry";
    }
    
    // Store a dict of parameters to be used by the gui and saving into json.
    geometry.parameters = {"width":width, "h":h, "s":s, "t":t, "b":b};
    return geometry;
}


export {geometryDetails, generateBeam};