
vert_shader = """
#version 120

attribute vec2 a_position;
attribute float a_height;

void main(void) {

    // map points [-1, 1] to points [1, 0]
    // 1 is the farthest coordinate, 0 - the closest
    float z = (1 - a_height) * 0.5;
    gl_Position = vec4(a_position.xy, z, z);
}
"""

frag_shader = """
#version 120

void main(void) {
    gl_FragColor = vec4(0.5, 0.5, 1, 1);
}
"""