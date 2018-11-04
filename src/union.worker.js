import union from '@turf/union'
import circle from '@turf/circle'


self.addEventListener('message', msg => {
	let points = msg.data['points']
	let radius = msg.data['radius'] / 1000

	function make_circle(point) {
		return circle([point['lat'], point['lon']], radius)
	}

	let all = make_circle(points[0])

	points.forEach(point => all = union(all, make_circle(point)))
	postMessage(all.geometry.coordinates)
})