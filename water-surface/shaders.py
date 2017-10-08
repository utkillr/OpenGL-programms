
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
    
    // map points [-1, 1] to points [1, 0]
    // 1 is the farthest coordinate, 0 - the closest
    v_z = (1 - a_height) * 0.5;
    
    // pass normal to fragments shader
    v_normal = normalize(vec3(a_normal, -1));
    // pass position to fragments shader
    v_position = vec3(a_position.xy, a_height);

    // last coordinate is 1 to turn off perspective 
    // (heat map is 2D)
    gl_Position = vec4(a_position.xy / 2, a_height*v_z, v_z);
}
"""

frag_shader_triangle = """
#version 120

varying vec3 v_normal;
varying vec3 v_position;

uniform vec3 u_sun_direction;
uniform vec3 u_sun_color;
uniform vec3 u_ambient_color;
uniform sampler2D u_sky_texture;

void main(void) {
    // camera is in point 'eye'
    vec3 eye = vec3(0, 0, 1);
    vec3 to_eye = normalize(v_position - eye);
    
    // count direction vector of reflected camera beam
    vec3 reflected = normalize(to_eye - 2 * v_normal * dot(v_normal, to_eye) / dot(v_normal, v_normal));
    
    vec2 texture_coord = 0.25 * reflected.xy / reflected.z + (0.5, 0.5);
    vec3 sky_color = texture2D(u_sky_texture, texture_coord).rgb;
    
    // float directed_light = pow(max(0, -dot(u_sun_direction, reflected)), 16);
    
    // Color is a summary of directed and diffuse colors
    // If brightness is very big, cut off redundant
    // vec3 rgb = clamp(u_sun_color * directed_light + u_ambient_color, 0.0, 1.0);
    // gl_FragColor = vec4(rgb, 1);
    
    vec3 rgb = sky_color;
    gl_FragColor.rgb = clamp(rgb,0.0,1.0);
    gl_FragColor.a = 1;
    }
"""

frag_shader_point = """
#version 120

void main() {
    gl_FragColor = vec4(1, 0, 0, 1);
}
"""
