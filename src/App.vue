<template>
  <div id="app">
    <div id="settings">
        <div>
          <button v-on:click="locate">Locate</button>
        </div>

        Distance {{radius}}m: <input type="range" v-model="radius" min="10" max="10000">

        <div v-for="grp in Object.keys(points)">
          <input type="radio" name="group" :value="grp" v-model="group">
          {{grp}}
        </div>
    </div>

    <div id="map"></div>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import L from 'leaflet'
import points from './trams.js'
import Worker from 'worker-loader!./union.worker.js';
import home_svg from './assets/home.svg'

var home_icon = L.icon({
  iconUrl: home_svg,
  iconSize: [38, 95], // size of the icon
});


export default {
  name: 'app',
  components: {
    HelloWorld
  },

  data() {
    return {
      map: null,
      worker: null,
      radius: 500,
      points: points,
      group: Object.keys(points)[0],

      markers: [],
      location: null,
      polygons: null,
    }
  },

  watch: {
    radius(new_radius) {
        this.compute_radius(new_radius)
    },

    group() {
      this.place_markers()
    }
  },

  methods: {
    locate() {
      navigator.geolocation.getCurrentPosition(pos => {
        if(this.location) {
          this.map.removeLayer(this.location)
        }

        const coord = [pos.coords.latitude, pos.coords.longitude]
        this.map.setView(coord)
        this.location = L.marker(coord, {icon: home_icon})
            .addTo(this.map)
            .bindPopup('Your location')
        })
    },

    current_points() {
      return this.points[this.group]
    },

    compute_radius() {
      this.new_worker()
      this.worker.postMessage({'points': this.current_points(), 'radius': this.radius})
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
    },

    place_markers() {
      if(this.polygons) {
          this.map.removeLayer(this.polygons)
      }

      this.compute_radius()

      this.markers.forEach((i) => this.map.removeLayer(i))
      this.markers = this.current_points().map((stop) => L.marker([stop['lat'], stop['lon']])
        .addTo(this.map)
        .bindPopup(stop['name'])
      )
    }
  },

  mounted() {
    this.map = L.map('map').setView([49.83465, 18.28204], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(this.map)

    this.place_markers()
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