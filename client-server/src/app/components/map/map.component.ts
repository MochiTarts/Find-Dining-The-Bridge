import { environment } from '../../../environments/environment';
import { Component, OnInit, Input, OnChanges, SimpleChanges } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import * as mapboxgl from 'mapbox-gl';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss'],
})
export class MapComponent implements OnInit, OnChanges {
  @Input() restaurants: any;
  @Input() userId: string;
  @Input() role: string;

  map: mapboxgl.Map;

  lat = 43.7839;
  lng = -79.1874;

  sc_lat = 43.774578;
  sc_lng = -79.252357;

  currentMarkers = [];

  constructor(
    private route: ActivatedRoute,
  ) { }

  ngOnChanges(changes: SimpleChanges): void {
    let currentRestaurants = changes.restaurants.currentValue;

    if (!changes.restaurants.firstChange) {
      this.updateMap(currentRestaurants);
    }
  }

  ngOnInit() {
    let GEO_location = {lat: null, lng: null};
    if (this.route.snapshot.queryParams.GEO_location) {
      GEO_location = JSON.parse(this.route.snapshot.queryParams.GEO_location.replace(/\'/g, '"'));
    }
    let centered_lat = GEO_location.lat || this.sc_lat;
    let centered_lng = GEO_location.lng || this.sc_lng;

    var options = {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0,
    };

    Object.getOwnPropertyDescriptor(mapboxgl, 'accessToken').set(
      environment.mapbox.accessToken
    );

    var style = 'mapbox://styles/mapbox/streets-v11';

    this.map = new mapboxgl.Map({
      container: 'map',
      style: style,
      zoom: 13,
      center: [centered_lng, centered_lat],
    });

    // Add map controls
    this.map.addControl(new mapboxgl.NavigationControl());

    var popup = new mapboxgl.Popup().setHTML('<p tabindex="0">Scarborough</p>');

    // Add map markers
    var marker = new mapboxgl.Marker({ color: '#0000FF' })
      .setLngLat([this.sc_lng, this.sc_lat])
      .setPopup(popup)
      .addTo(this.map);

    popup.on('close', () => {
      marker.getElement().focus();
    })

    this.updateMap(this.restaurants);
  }

  updateMap(restaurants) {
    for (let marker of this.currentMarkers) {
      marker.remove();
    }

    this.currentMarkers = [];

    for (let index of restaurants) {
      if (index.GEO_location != 'blank') {
        var GEOJson = JSON.parse(index.GEO_location.replace(/\'/g, '"'));
      }

      if (index.GEO_location != 'blank' && GEOJson.lng != undefined) {
        let cuisineList: string = '';
        for (let cuisine of index.cuisines) {
          if (cuisineList == '') {
            cuisineList = String(cuisine);
          } else {
            cuisineList = cuisineList + ", " + String(cuisine);
          }
        }

        var popup = new mapboxgl.Popup().setHTML(`
            <div tabindex="0"><h2>${index.name}</h2>
              ${index.address}
              <br/>
              ${index.phone}
              <br/>
              ${cuisineList}
              <br/>
              <a class="btn" href="/restaurant?restaurantId=${index._id}&userId=${this.userId}&role=${this.role}"> View Restaurant </a>
            </div>`
        );

        let marker = new mapboxgl.Marker({ color: '#165788' })
          .setLngLat([GEOJson.lng, GEOJson.lat])
          .setPopup(popup)
          .addTo(this.map);

        this.currentMarkers.push(marker);

        popup.on('close', () => {
          marker.getElement().focus();
        });

      }
    }
  }

  error(err) { }
}