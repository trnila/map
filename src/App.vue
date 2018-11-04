<template>
  <div id="app">
    <div id="settings">
        Distance {{radius}}m: <input type="range" v-model="radius" min="10" max="10000">

        <button v-on:click="locate">Locati</button>
    </div>

    <div id="map"></div>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import L from 'leaflet'
import trams from './trams.js'
import Worker from 'worker-loader!./union.worker.js';
import home_svg from './assets/home.svg'


export default {
  name: 'app',
  components: {
    HelloWorld
  },

  data() {
    return {
      map: null,
      worker: null,
      polygons: null,
      radius: 500,
      location: null,
    }
  },

  watch: {
    radius(new_radius) {
        this.compute_radius(new_radius)
    }
  },

  methods: {
    locate() {
      navigator.geolocation.getCurrentPosition(pos => {
        if(this.location) {
          this.map.removeLayer(self.location)
        }

        var firefoxIcon = L.icon({
        iconUrl: home_svg,
        iconSize: [38, 95], // size of the icon
        });

        const coord = [pos.coords.latitude, pos.coords.longitude]
        this.map.setView(coord)
        this.location = L.marker(coord, {icon: firefoxIcon})
            .addTo(this.map)
            .bindPopup('Your location')
        })
    },

    compute_radius() {
      this.new_worker()
      this.worker.postMessage({'points': trams, 'radius': this.radius})
    },

    new_worker() {
      if(this.worker) {
        this.worker.terminate()
      }
      this.worker = new Worker();

      this.worker.addEventListener('message', msg => {
        if(this.polygons) {
          this.map.removeLayer(this.polygons)
        }

        this.polygons = L.polygon(msg.data).addTo(this.map)
      })
    }
  },

  mounted() {
    this.map = L.map('map').setView([49.83465, 18.28204], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(this.map)

    this.compute_radius()

    trams.forEach((stop) => L.marker([stop['lat'], stop['lon']])
      .addTo(this.map)
      .bindPopup(stop['name'])
    )
  }
}
</script>

<style>
html, body, #app, #map {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0
}

#settings {
  position: absolute;
  z-index: 1000;
  right: 0px;
  top: 0px;
  background: rgba(255, 255, 255, 0.9);
  padding: 15px;
}
</style>