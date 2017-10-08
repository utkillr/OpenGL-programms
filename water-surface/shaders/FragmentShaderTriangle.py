frag_shader_triangle = """
#version 120

varying vec3 v_normal;
varying vec3 v_position;

uniform vec3 u_sun_direction;
uniform vec3 u_sun_color;
uniform vec3 u_ambient_color;
uniform sampler2D u_sky_texture;
uniform sampler2D u_bed_texture;
uniform float u_alpha;
uniform float u_bed_depth;
uniform float u_eye_height;

void main(void) {
    // camera is in point 'eye'
    vec3 eye = vec3(0, 0, u_eye_height);
    vec3 from_eye = normalize(v_position - eye);

    // count direction vector of reflected camera beam
    vec3 normal = normalize(-v_normal);
    vec3 reflected = normalize(from_eye - 2 * normal * dot(normal, from_eye));

    vec2 texture_coord = 0.25 * reflected.xy / reflected.z + (0.5, 0.5);
    vec3 sky_color = texture2D(u_sky_texture, texture_coord).rgb;

    // float directed_light = pow(max(0, -dot(u_sun_direction, reflected)), 16);
    // Color is a summary of directed and diffuse colors
    // If brightness is very big, cut off redundant
    // vec3 rgb = clamp(u_sun_color * directed_light + u_ambient_color, 0.0, 1.0);
    // gl_FragColor = vec4(rgb, 1);
    
    // what the hell is c, d, cr? Why cross?
    vec3 cr = cross(normal, from_eye);
    float d = 1 - u_alpha * u_alpha * dot(cr, cr);
    float c2 = sqrt(d);
    vec3 refracted = normalize(u_alpha * cross(cr, normal) - normal * d);
    float c1 = -dot(normal, from_eye);
    
    // dont give a fuck what's going on here
    float t = (-u_bed_depth - v_position.z) / refracted.z;
    vec3 point_on_bed = v_position + t * refracted;
    vec2 bed_texcoord = point_on_bed.xy + vec2(0.5, 0.5);
    vec3 bed_color = texture2D(u_bed_texture, bed_texcoord).rgb;

    float reflectance_s = pow((u_alpha * c1 - c2) / (u_alpha * c1 + c2), 2);
    float reflectance_p = pow((u_alpha * c2 - c1) / (u_alpha * c2 + c1), 2);
    float reflectance = (reflectance_s + reflectance_p) / 2;

    float diw = length(point_on_bed - v_position);
    vec3 filter = vec3(1, 0.5, 0.2);
    vec3 mask = vec3(exp(-diw * filter.x), exp(-diw * filter.y), exp(-diw * filter.z));
    vec3 ambient_water = vec3(0, 0.6, 0.8);
    vec3 image_color = bed_color * mask + ambient_water * (1 - mask);

    vec3 rgb = sky_color * reflectance + image_color * (1 - reflectance);
    
    // up to here

    // vec3 rgb = sky_color;
    gl_FragColor.rgb = clamp(rgb,0.0,1.0);
    gl_FragColor.a = 1;
}
"""
