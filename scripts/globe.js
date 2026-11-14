
function initializeGlobe(container) {

    const world = Globe()(container)

        // Globe appearance
        .globeImageUrl(null)
        .backgroundColor('#000000')
        .showAtmosphere(false)
        .showGraticules(true)

        // Camera
        .pointOfView({
            lat: 20,
            lng: 0,
            altitude: 2.5
        });

    // Remove default lighting
    world.lights([]);

    // Load country boundaries
    fetch(
        'https://raw.githubusercontent.com/vasturiano/globe.gl/master/example/datasets/ne_110m_admin_0_countries.geojson'
    )
        .then(response => {
            if (!response.ok) {
                throw new Error('Could not load country data');
            }
            return response.json();
        })
        .then(countries => {

            world
                .polygonsData(countries.features)
                .polygonAltitude(0.001)
                .polygonCapColor(() => 'rgba(0,0,0,0)')
                .polygonSideColor(() => 'rgba(0,0,0,0)')
                .polygonStrokeColor(() => '#FFFFFF')
                .polygonLabel(({ properties }) =>
                    properties.ADMIN
                );
        })
        .catch(error => {
            console.error('Country loading error:', error);
        });

    // Rotation
    world.controls().autoRotate = true;
    world.controls().autoRotateSpeed = 0.35;
    world.controls().enableZoom = true;

    return world;
}
