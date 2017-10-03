
vert_shader = """
#version 120

attribute vec2 a_position;
attribute float a_height;

// varying to be able to use v_z in fragment shader
varying float v_z;

void main(void) {
    
    // map points [-1, 1] to points [1, 0]
    // 1 is the farthest coordinate, 0 - the closest
    v_z = (1 - a_height) * 0.5;

    // last coordinate is 1 to turn off perspective 
    // (heat map is 2D)
    gl_Position = vec4(a_position.xy, v_z, 1);
}
"""

frag_shader = """
#version 120

varying float v_z;

void main(void) {
    // some random color
    vec3 rgb = vec3(0.12, 0.44, v_z);

    gl_FragColor = vec4(rgb, 1);
}
"""
