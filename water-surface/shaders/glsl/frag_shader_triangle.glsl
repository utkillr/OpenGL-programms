#version 120

varying vec3 v_normal;
varying vec3 v_position;
varying vec3 v_reflected;
varying vec2 v_sky_texture_coord;
varying vec2 v_bed_texture_coord;
varying float v_reflectance;
varying vec3 v_mask;

uniform sampler2D u_sky_texture;
uniform sampler2D u_bed_texture;
uniform vec3 u_sun_direction;
uniform vec3 u_sun_diffused_color;
uniform vec3 u_sun_reflected_color;

uniform float u_reflected_mult;
uniform float u_diffused_mult;
uniform float u_bed_mult;
uniform float u_depth_mult;
uniform float u_sky_mult;

void main() {
    vec3 sky_color = texture2D(u_sky_texture, v_sky_texture_coord).rgb;
    vec3 bed_color = texture2D(u_bed_texture, v_bed_texture_coord).rgb;

    vec3 normal = normalize(v_normal);
    float diffused_intensity = u_diffused_mult * max(0, -dot(normal, u_sun_direction));
    float cos_angle = max(0, dot(u_sun_direction, normalize(v_reflected)));
    float reflected_intensity = u_reflected_mult * pow(cos_angle, 100);

    vec3 ambient_water = vec3(0, 0.3, 0.5);
    vec3 image_color = u_bed_mult * bed_color * v_mask + u_depth_mult * ambient_water * (1 - v_mask);

    float sky_mult = u_sky_mult;
    float reflectance = v_reflectance;

    if (1 - reflectance < 0) {
        reflectance = 0;
        reflected_intensity = 0;
        diffused_intensity = 0;
        sky_mult = 0;
    }

    vec3 rgb = sky_mult * sky_color * reflectance + image_color * (1 - reflectance)
        + diffused_intensity * u_sun_diffused_color + reflected_intensity * u_sun_reflected_color;

    gl_FragColor.rgb = clamp(rgb,0.0,1.0);
    gl_FragColor.a = 1;
}
