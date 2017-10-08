
vert_shader = """
#version 120

attribute vec2 a_position;
attribute float a_height;
attribute vec2 a_normal;

uniform vec3 u_sun_direction;
varying float v_directed_light;

// varying to be able to use v_z in fragment shader
varying float v_z;

void main(void) {
    
    // map points [-1, 1] to points [1, 0]
    // 1 is the farthest coordinate, 0 - the closest
    v_z = (1 - a_height) * 0.5;
    
    // count cosine between normal to surface and sun direction
    vec3 normal = normalize(vec3(a_normal, -1));
    v_directed_light = max(0, -dot(normal, u_sun_direction));

    // last coordinate is 1 to turn off perspective 
    // (heat map is 2D)
    gl_Position = vec4(a_position.xy, a_height*v_z, v_z);
}
"""

frag_shader = """
#version 120

varying float v_z;
varying float v_directed_light;

uniform vec3 u_sun_color;
uniform vec3 u_ambient_color;

void main(void) {
    // Color is a summary of directed and ambient colors
    // If brightness is very big, cut off redundant
    vec3 rgb = clamp(u_sun_color * v_directed_light + u_ambient_color, 0.0, 1.0);

    gl_FragColor = vec4(rgb, 1);
}
"""
