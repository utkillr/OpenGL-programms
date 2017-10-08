
vert_shader = """
#version 120

attribute vec2 a_position;
attribute float a_height;
attribute vec2 a_normal;

varying vec3 v_normal;
varying vec3 v_position;

// varying to be able to use v_z in fragment shader
varying float v_z;

void main(void) {
    // pass normal to fragments shader
    v_normal = normalize(vec3(a_normal, -1));
    // pass position to fragments shader
    v_position = vec3(a_position.xy, a_height);

    // map points [-1, 1] to points [1, 0]
    // 1 is the farthest coordinate, 0 - the closest
    v_z = (1 - a_height) * 0.5;
    // last coordinate is 1 to turn off perspective 
    // (heat map is 2D)
    gl_Position = vec4(a_position.xy, a_height*v_z, v_z);
}
"""