let sections = document.querySelectorAll('section');

let options = {
    rootMargin: '0px',
    threshold: 0.25
}

const callback = (entries) => {
    entries.forEach((entry) => {
        const { target } = entry;
        if (entry.intersectionRatio >= 0.25) {
            target.classList.add('is-visible');
        } else {
            target.classList.remove('is-visible');
        }
    })
}

const observer = new IntersectionObserver(callback, options)

sections.forEach((section, index) => {
    observer.observe(section)
})


function geoFindMe() {

    const status = document.querySelector('#status');
    const mapLink = document.querySelector('#map-link');

    mapLink.href = '';
    mapLink.textContent = '';

    function success(position) {
        const latitude  = position.coords.latitude;
        const longitude = position.coords.longitude;

        status.textContent = '';
        mapLink.href = `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;
        mapLink.textContent = `Latitude: ${latitude} °, Longitude: ${longitude} °`;
    }

    function error() {
        status.textContent = 'Unable to retrieve your location';
    }

    if(!navigator.geolocation) {
        status.textContent = 'Geolocation is not supported by your browser';
    } else {
        status.textContent = 'Locating…';
        navigator.geolocation.getCurrentPosition(success, error);
    }

}

document.querySelector('#location').addEventListener('click', geoFindMe);


document.getElementsByClassName('box-9')[0].addEventListener('click', function (){
    document.querySelector('.wave').classList.toggle('active');
    generateConfig();
    setTimeout(() => location.replace('/'), 2000);
});




