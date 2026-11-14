const THREE = window.THREE;
function initializeGlobe(container, attacks) {

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
    // world.lights([]); --THIS EATS ALL LIGHTS OF THE WORLD!!

    // method 2 to keep ambient lighting and remove da sun

    const ambientLights = world.lights().filter(
        light => light.type === "AmbientLight"
    );
    world.lights(ambientLights);

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
    // Attack locations
    world
        .pointsData(attacks) //Supplies attack records
        .pointLat("latitude")   //Reads latitude
        .pointLng("longitude")  //"" Longitude
        .pointColor(() => "#ff2424") //RED RED RED
        .pointAltitude(0.015) //gives the marker height
        .pointRadius(0.2) //marker size
        .pointsMerge(false);






    // Rotation //

    const controls = world.controls();

    controls.autoRotate = true;
    controls.autoRotateSpeed = -0.35;
    controls.enableZoom = true;

    let idleTimer;

    // Resume rotation 10 seconds after interaction
    function resumeRotationAfterIdle() {
        clearTimeout(idleTimer);

        idleTimer = setTimeout(() => {
            controls.autoRotate = true;
        }, 30000); //This is counted in miliseconds, 10k ms is 10 s
    }

    // Stop rotation and restart the countdown
    function stopRotation() {
        controls.autoRotate = false;
        resumeRotationAfterIdle();
    }

    // Detect user interaction
    container.addEventListener('pointerdown', stopRotation);

    container.addEventListener('pointermove', (event) => {
        if (event.buttons > 0) {
            stopRotation();
        }
    });

    container.addEventListener('wheel', stopRotation);
    container.addEventListener('touchstart', stopRotation);

    return world;
}
