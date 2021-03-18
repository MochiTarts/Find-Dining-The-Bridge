import { Component, OnInit } from '@angular/core';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { RestaurantService } from '../_services/restaurant.service';
import { geolocation } from '../utils/geolocation';
import { cuisinesStr } from '../constants/cuisines';
import { Title } from '@angular/platform-browser';



@Component({
  selector: 'app-all-restaurants',
  templateUrl: './all-restaurants.component.html',
  styleUrls: ['./all-restaurants.component.scss'],
})
export class AllRestaurantsComponent implements OnInit {
  userId: string = '';
  role: string = '';

  allRestaurants: any[];
  allDishes: any[];
  allCuisines: any[];
  restaurants_total;

  priceFilterRestaurants: any[];
  deliveryFilterRestaurants: any[];
  cuisineFilterRestaurants: any[];
  searchedRestaurants: any[];

  restaurants: any[];
  dishes: any[];
  inputRestaurant: string = '';
  inputDishes: string = '';

  LONGITUDE_PROPERTY_NAME: string = 'lng';
  LATITUDE_PROPERTY_NAME: string = 'lat';

  faSearch = faSearch;

  constructor(
    private restaurantService: RestaurantService,
    private titleService: Title 
  ) {}

  ngOnInit(): void {
    this.loadRestaurants();
    //this.loadDishes();
    this.allCuisines = cuisinesStr;
    this.titleService.setTitle("Browse | Find Dining Scarborough"); 
  }

  loadRestaurants() {
    this.restaurantService.listRestaurants().subscribe((data) => {
      this.restaurants = data.Restaurants;
      this.allRestaurants = data.Restaurants;
      navigator.geolocation.getCurrentPosition((positon) => {
        for (var i = 0; i < this.restaurants.length; i++) {
          var index = this.restaurants[i];

          if (index.GEO_location != 'blank' && index.GEO_location != '') {
            var GEOJson = JSON.parse(index.GEO_location.replace(/\'/g, '"'));
            if (
              GEOJson[this.LONGITUDE_PROPERTY_NAME] != undefined &&
              GEOJson[this.LATITUDE_PROPERTY_NAME] != undefined
            ) {
              this.restaurants[
                i
              ].distanceFromUser = geolocation.haversineDistance(
                GEOJson[this.LATITUDE_PROPERTY_NAME],
                GEOJson[this.LONGITUDE_PROPERTY_NAME],
                positon.coords.latitude,
                positon.coords.longitude
              );
            }
          }
        }
        this.restaurants = this.sortClosestCurrentLoc(this.restaurants);
        this.allRestaurants = this.restaurants;
      });
      this.restaurants_total = this.allRestaurants.length;
      this.priceFilterRestaurants = this.allRestaurants;
      this.deliveryFilterRestaurants = this.allRestaurants;
      this.cuisineFilterRestaurants = this.allRestaurants;
      this.searchedRestaurants = this.allRestaurants;
    });
  }

  loadDishes() {
    this.restaurantService.getDishes().subscribe((data) => {
      this.dishes = data.Dishes;
      this.allDishes = data.Dishes;
    });
  }

  updateRestarants() {
    this.restaurants = [];
    console.log(this.priceFilterRestaurants)
    for (var i = 0; i < this.priceFilterRestaurants.length; i++) {
      var current = this.priceFilterRestaurants[i];
      if (this.deliveryFilterRestaurants.includes(current)
          && this.cuisineFilterRestaurants.includes(current)
          && this.searchedRestaurants.includes(current))
      {
        this.restaurants.push(current);
      }
    }
  }

  sortClosestCurrentLoc(restaurants: Array<any>) {
    return restaurants.sort((rest1, rest2) => {
      let result = 0;
      let valid1 = rest1.hasOwnProperty('distanceFromUser');
      let valid2 = rest2.hasOwnProperty('distanceFromUser');
      if (!valid1 && valid2) return 0;
      // if only one is invalid, return a really high weight in direction of the valid one
      if (!valid1) {
        return 1000;
      }
      if (!valid2) {
        return -1000;
      }
      return rest1.distanceFromUser - rest2.distanceFromUser;
    });
  }

  // This is for the enter key press on check boxes.
  filterEnter(event){
    event.srcElement.click();
  }

  filterPricepoint(list) {
    const isFalse = (currentValue) => !currentValue;
    if (list.every(isFalse)) {
      this.priceFilterRestaurants = this.allRestaurants;
    } else {
      this.priceFilterRestaurants = [];
      for (var i = 0; i < this.allRestaurants.length; i++) {
        var query = this.allRestaurants[i];
        if (list[0] == true && query.pricepoint == 'LOW') {
          this.priceFilterRestaurants.push(query);
        }

        if (list[1] == true && query.pricepoint == 'MID') {
          this.priceFilterRestaurants.push(query);
        }

        if (list[2] == true && query.pricepoint == 'HIGH') {
          this.priceFilterRestaurants.push(query);
        }

        if (list[3] == true && query.pricepoint == 'EXHIGH' ){
          this.priceFilterRestaurants.push(query);
        }
      }
    }
    this.updateRestarants();
  }

  filterDeliveryCharges(list) {
    // const isFalse = (currentValue) => !currentValue;

    // if (list.every(isFalse)) {
    //   this.deliveryFilterRestaurants = this.allRestaurants;
    // } else {
    //   this.deliveryFilterRestaurants = [];
    //   for (var i = 0; i < this.allRestaurants.length; i++) {
    //     var query = this.allRestaurants[i];
    //     if (list[0] == true && query.deliveryFee == '$1 - $2') {
    //       this.deliveryFilterRestaurants.push(query);
    //     }

    //     if (list[1] == true && query.deliveryFee == '$2 - $4') {
    //       this.deliveryFilterRestaurants.push(query);
    //     }

    //     if (list[2] == true && query.deliveryFee == '$5+') {
    //       this.deliveryFilterRestaurants.push(query);
    //     }
    //   }
    // }
    // this.updateRestarants();
  }

  filterCuisine(list) {
    const isFalse = (currentValue) => !currentValue;

    if (list.every(isFalse)) {
      this.cuisineFilterRestaurants = this.allRestaurants;
    } else {
      this.cuisineFilterRestaurants = [];
      for (var i = 0; i < this.allRestaurants.length; i++) {
        var query = this.allRestaurants[i];
        for (var j = 0; j < this.allCuisines.length; j++) {
          if (list[j] == true && query.cuisines.includes(this.allCuisines[j])) {
            this.cuisineFilterRestaurants.push(query);
            break;
          }
        }
      }
    }
    this.updateRestarants();
  }

  filterPrice(list) {
    this.dishes = [];
    const isFalse = (currentValue) => !currentValue;

    if (list.every(isFalse)) {
      this.dishes = this.allDishes;
    } else {
      for (var i = 0; i < this.allDishes.length; i++) {
        var query = this.allDishes[i];
        if (list[0] == true && query.price <= 20) {
          this.dishes.push(query);
        }

        if (list[1] == true && query.price > 20 && query.price <= 40) {
          this.dishes.push(query);
        }

        if (list[2] == true && query.price > 40 && query.price <= 60) {
          this.dishes.push(query);
        }

        if (list[3] == true && query.price > 60) {
          this.dishes.push(query);
        }
      }
    }
  }

  searchRestaurants() {
    if (this.inputRestaurant == '') {
      this.searchedRestaurants = this.allRestaurants;
    } else {
      this.searchedRestaurants = [];
      for (var i = 0; i < this.allRestaurants.length; i++) {
        var query = this.allRestaurants[i];
        if (
          query.name
            .toLowerCase()
            .includes(this.inputRestaurant.toLowerCase()) ||
          query.cuisines.toString()
            .toLowerCase()
            .includes(this.inputRestaurant.toLowerCase()) ||
          query.pricepoint
            .toLowerCase()
            .includes(this.inputRestaurant.toLowerCase()) 
        ) {
          this.searchedRestaurants.push(query);
        }
      }
    }
    this.updateRestarants();
  }

  searchDishes() {
    if (this.inputDishes == '') {
      this.dishes = this.allDishes;
    } else {
      this.dishes = [];
      for (var i = 0; i < this.allDishes.length; i++) {
        var query = this.allDishes[i];
        if (
          query.name.toLowerCase().includes(this.inputDishes.toLowerCase()) ||
          query.price.toLowerCase().includes(this.inputDishes.toLowerCase())
        ) {
          this.dishes.push(query);
        }
      }
    }
  }
}
