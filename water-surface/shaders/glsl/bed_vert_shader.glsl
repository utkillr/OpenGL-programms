#version 120

uniform float u_eye_height;
uniform mat4 u_world_view;

attribute float a_bed_depth;
attribute vec2 a_position;
attribute vec2 a_normal;

varying vec3 v_position;
varying vec2 v_bed_texture_coord;

// varying to be able to use v_z in fragment shader
varying float v_z;

void main() {
    v_position = vec3(a_position.xy, a_bed_depth);
    v_bed_texture_coord = v_position.xy + vec2(0.5, 0.5);

    // new code
    vec4 position_view = u_world_view * vec4(v_position, 1);
    float z = 1 - (1 + position_view.z) / (1 + u_eye_height);
    gl_Position = vec4(position_view.xy, -position_view.z*z, z);
}