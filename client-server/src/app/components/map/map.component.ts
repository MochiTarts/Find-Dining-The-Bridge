import { environment } from '../../../environments/environment';
import { Component, OnInit, Input, OnChanges, SimpleChanges } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import * as mapboxgl from 'mapbox-gl';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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

  location: string = '';

  GEO_location = { lat: null, lng: null };
  isQueryLocation: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
  ) { }

  ngOnChanges(changes: SimpleChanges): void {
    let currentRestaurants = changes.restaurants.currentValue;

    if (!changes.restaurants.firstChange) {
      this.updateMap(currentRestaurants);
    }
  }

  ngOnInit() {
    if (this.route.snapshot.queryParams.GEO_location) {
      this.GEO_location = JSON.parse(this.route.snapshot.queryParams.GEO_location.replace(/\'/g, '"'));
      this.isQueryLocation = true;
    }

    if (this.route.snapshot.queryParams.location) {
      this.location = this.route.snapshot.queryParams.location;
    }

    let centered_lat = this.GEO_location.lat || this.sc_lat;
    let centered_lng = this.GEO_location.lng || this.sc_lng;

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
      zoom: 12,
      center: [centered_lng, centered_lat],
    });

    // Add map controls
    this.map.addControl(new mapboxgl.NavigationControl());

    var popup = new mapboxgl.Popup().setHTML('<p tabindex="0">Scarborough</p>');

    // Add map markers
    var marker = new mapboxgl.Marker({ color: '#0000FF' })
      .setLngLat([this.sc_lng, this.sc_lat])
      .setPopup(popup)
      .addTo(this.map)
      .togglePopup();

    popup.on('close', () => {
      marker.getElement().focus();
    });

    if (this.location) {

      this.getGeoCode(this.location).subscribe((data) => {
        let selectedLocation = data["features"][0];
        let newCenter = {
          longitude: selectedLocation.center[0],
          latitude: selectedLocation.center[1],
        };

        var queryLocationPopup = new mapboxgl.Popup().setHTML(`<p tabindex="0">${selectedLocation.place_name}</p>`);

        // Add map markers
        var queryLocationMarker = new mapboxgl.Marker({ color: '#027bff' })
          .setLngLat([newCenter.longitude, newCenter.latitude])
          .setPopup(queryLocationPopup)
          .addTo(this.map);

        queryLocationPopup.on('close', () => {
          queryLocationMarker.getElement().focus();
        });

        // Set query location as center of map
        this.map.setCenter(new mapboxgl.LngLat(newCenter.longitude, newCenter.latitude));
      })

    }


    this.updateMap(this.restaurants);
  }

  /**
   * Gets the location marker on the map of the searched address
   * @param searchText - the searched address
   * @returns the Observable from the http request
   */
  getGeoCode(searchText: string): Observable<any> {
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${searchText}.json?country=ca&types=place,address,neighborhood,locality&access_token=${environment.mapbox.accessToken}`;
    return this.http.get(url);
  }

  /**
   * Updates the location markers on the map given the list of restaurants
   * @param restaurants - list of restaurants
   */
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

        if (this.isQueryLocation && this.GEO_location.lat == GEOJson.lat && this.GEO_location.lng == GEOJson.lng) {
          marker.togglePopup();
        }

        this.currentMarkers.push(marker);

        popup.on('close', () => {
          marker.getElement().focus();
        });

      }
    }
  }

  error(err) { }
}
