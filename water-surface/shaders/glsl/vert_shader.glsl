#version 120

uniform float u_eye_height;
uniform mat4 u_world_view;
uniform float u_alpha;
// uniform float u_bed_depth;

attribute float a_bed_depth;
attribute vec2 a_position;
attribute float a_height;
attribute vec2 a_normal;

varying vec3 v_normal;
varying vec3 v_position;
varying vec3 v_reflected;
varying vec2 v_sky_texture_coord;
varying vec2 v_bed_texture_coord;
varying float v_reflectance;
varying vec3 v_mask;

// varying to be able to use v_z in fragment shader
varying float v_z;

void main() {
    // pass normal to fragments shader
    v_normal = normalize(vec3(a_normal, -1));
    // pass position to fragments shader
    v_position = vec3(a_position.xy, a_height);

    // new code
    vec4 position_view = u_world_view * vec4(v_position, 1);
    float z = 1 - (1 + position_view.z) / (1 + u_eye_height);
    gl_Position = vec4(position_view.xy, -position_view.z*z, z);

    vec4 eye_view = vec4(0, 0, u_eye_height, 1);
    vec4 eye = transpose(u_world_view) * eye_view;
    vec3 from_eye = normalize(v_position - eye.xyz);

    // count direction vector of reflected camera beam
    vec3 normal = normalize(-v_normal);
    v_reflected = normalize(from_eye - 2 * normal * dot(normal, from_eye));

    v_sky_texture_coord = 0.05 * v_reflected.xy / v_reflected.z + vec2(0.5, 0.5);

    // dont give a fuck what's going on here
    vec3 cr = cross(normal, from_eye);
    float d = 1 - u_alpha * u_alpha * dot(cr, cr);
    float c2 = sqrt(d);
    vec3 refracted = normalize(u_alpha * cross(cr, normal) - normal * c2);
    float c1 = -dot(normal, from_eye);

    float t = (-a_bed_depth - v_position.z) / refracted.z;
    vec3 point_on_bed = v_position + t * refracted;
    v_bed_texture_coord = point_on_bed.xy + vec2(0.5, 0.5);

    float reflectance_s = pow((u_alpha * c1 - c2) / (u_alpha * c1 + c2), 2);
    float reflectance_p = pow((u_alpha * c2 - c1) / (u_alpha * c2 + c1), 2);
    v_reflectance = (reflectance_s + reflectance_p) / 2;

    float diw = length(point_on_bed - v_position);
    vec3 my_filter = vec3(1, 0.5, 0.2);
    v_mask = vec3(exp(-diw * my_filter.x), exp(-diw * my_filter.y), exp(-diw * my_filter.z));
}
