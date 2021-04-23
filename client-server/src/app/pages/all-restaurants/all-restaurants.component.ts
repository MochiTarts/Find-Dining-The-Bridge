import { Component, OnInit } from '@angular/core';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { RestaurantService } from '../../_services/restaurant.service';
import { geolocation } from '../../utils/geolocation';
import { cuisinesStr } from '../../_constants/cuisines';
import { servicesStr } from '../../_constants/services';
import { Title } from '@angular/platform-browser';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';


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
  allServices: any[];
  restaurants_total;
  favList: any[] = [];

  priceFilterRestaurants: any[];
  deliveryFilterRestaurants: any[];
  cuisineFilterRestaurants: any[];
  serviceFilterRestaurants: any[];
  searchedRestaurants: any[];

  restaurants: any[] = [];
  dishes: any[];
  inputRestaurant: string = '';
  inputDishes: string = '';

  LONGITUDE_PROPERTY_NAME: string = 'lng';
  LATITUDE_PROPERTY_NAME: string = 'lat';

  faSearch = faSearch;

  location: string = '';
  show: number = 3;

  constructor(
    private restaurantService: RestaurantService,
    private titleService: Title,
    private tokenStorage: TokenStorageService,
    private userService: UserService,
    private route: ActivatedRoute,
    private http: HttpClient,
  ) { }

  ngOnInit(): void {
    var user = this.tokenStorage.getUser();
    this.userId = user.user_id;
    this.role = user.role;

    if (this.route.snapshot.queryParams.location) {
      this.location = this.route.snapshot.queryParams.location;
    }

    if (this.route.snapshot.queryParams.find) {
      this.inputRestaurant = this.route.snapshot.queryParams.find;
    }

    this.loadRestaurants();
    // this.loadDishes();

    if (this.userId != null && (this.role == 'BU' || this.role == 'RO')) {
      this.userService.getFavouriteRestaurants().subscribe((favs) => {
        this.favList = favs;
      })
    }

    this.allCuisines = cuisinesStr;
    this.allServices = servicesStr;
    this.titleService.setTitle("Browse | Find Dining Scarborough");
  }

  /**
   * Retrieves all approved restaurants
   */
  loadRestaurants() {
    this.restaurantService.listRestaurants().subscribe((data) => {
      this.restaurants = data.Restaurants;
      this.allRestaurants = data.Restaurants;
      this.initializeRestaurants();

      var selectedPostion: any;
      if (this.location) {
        this.getGeoCode(this.location).subscribe((data) => {
          let selectedLocation = data["features"][0];
          selectedPostion = {
            coords: {
              longitude: selectedLocation.center[0],
              latitude: selectedLocation.center[1],
            }
          };

          this.addDistance(selectedPostion);
          this.restaurants = this.sortClosestCurrentLoc(this.restaurants);
          console.log(this.restaurants);
          this.allRestaurants = this.restaurants;
          this.initializeRestaurants();

          if (this.inputRestaurant) {
            this.searchRestaurants();
          }
        });
      } else {
        navigator.geolocation.getCurrentPosition((position) => {
          selectedPostion = position;
          this.addDistance(selectedPostion);
          this.restaurants = this.sortClosestCurrentLoc(this.restaurants);
          this.allRestaurants = this.restaurants;
          this.initializeRestaurants();

          if (this.inputRestaurant) {
            this.searchRestaurants();
          }
        });
      }
    });
  }

  /**
   * Retrieves all approved dishes
   */
  loadDishes() {
    this.restaurantService.getDishes().subscribe((data) => {
      this.dishes = data.Dishes;
      this.allDishes = data.Dishes;
    });
  }

  /**
   * Sets the filter lists to be used when filtering restaurants
   */
  initializeRestaurants() {
    this.restaurants_total = this.allRestaurants.length;
    this.priceFilterRestaurants = this.allRestaurants;
    this.deliveryFilterRestaurants = this.allRestaurants;
    this.cuisineFilterRestaurants = this.allRestaurants;
    this.serviceFilterRestaurants = this.allRestaurants;
    this.searchedRestaurants = this.allRestaurants;
  }

  /**
   * Retrieves the location stamp of the searched restaurant's address
   * @param searchText - the searched address
   * @returns the Observable from the request
   */
  getGeoCode(searchText: string): Observable<any> {
    let newSearchText = searchText + ' Scarborough';
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${newSearchText}.json?country=ca&types=place,address,neighborhood,locality&access_token=${environment.mapbox.accessToken}`;
    return this.http.get(url);
  }

  /**
   * PLEASE UPDATE THIS DOCSTRING
   * @param selectedPostion - ?
   */
  addDistance(selectedPostion) {
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
            selectedPostion.coords.latitude,
            selectedPostion.coords.longitude
          );
        }
      }
    }
  }

  /**
   * Updates the list of restaurants to be displayed
   */
  updateRestarants() {
    this.restaurants = [];
    for (var i = 0; i < this.priceFilterRestaurants.length; i++) {
      var current = this.priceFilterRestaurants[i];
      if (this.deliveryFilterRestaurants.includes(current)
        && this.cuisineFilterRestaurants.includes(current)
        && this.serviceFilterRestaurants.includes(current)
        && this.searchedRestaurants.includes(current)) {
        this.restaurants.push(current);
      }
    }
  }

  /**
   * Sorts the restaurants by location, from closest to furthest
   *
   * @param restaurants - list of all approved restaurants
   * @returns The sorted list of restaurants
   */
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

  /**
   * Clicks the checkbox on enter key
   * @param event - the event that triggers this function
   */
  filterEnter(event) {
    event.srcElement.click();
  }

  /**
   * Updates the priceFilterRestaurants list based on the selected pricepoints. Then updates
   * the list of restaurants to display
   *
   * @param list - the list of bools representing which pricepoints were selected on the filter card
   */
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

        if (list[3] == true && query.pricepoint == 'EXHIGH') {
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

  /**
   * Updates the cuisineFilterRestaurants list based on the selected cuisines. Then updates
   * the list of restaurants to display
   *
   * @param list - the list of bools representing which cuisines were selected on the filter card
   */
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

  /**
   * Updates the serviceFilterRestaurants list based on the selected services. Then updates
   * the list of restaurants to display
   *
   * @param list - the list of bools representing which services were selected on the filter card
   */
  filterService(list) {
    const isFalse = (currentValue) => !currentValue;

    if (list.every(isFalse)) {
      this.serviceFilterRestaurants = this.allRestaurants;
    } else {
      this.serviceFilterRestaurants = [];
      for (let res of this.allRestaurants) {
        for (var j = 0; j < this.allServices.length; j++) {
          if (list[j] && res.offer_options.includes(this.allServices[j])) {
            this.serviceFilterRestaurants.push(res);
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

  /**
   * Updates the list of searchedRestaurants based on search
   * criteria
   */
  searchRestaurants() {
    if (this.inputRestaurant == '') {
      this.searchedRestaurants = this.allRestaurants;
    } else {
      this.searchedRestaurants = [];
      let keywords = this.inputRestaurant.toLowerCase().replace(',', ' ').split(' ');
      keywords = keywords.filter((value) => {
        return value != '';
      });

      for (var i = 0; i < this.allRestaurants.length; i++) {
        var query = this.allRestaurants[i];
        for (let keyword of keywords) {
          if (
            query.name
              .toLowerCase()
              .includes(keyword) ||
            query.cuisines.toString()
              .toLowerCase()
              .includes(keyword) ||
            query.offer_options.toString()
              .toLowerCase()
              .includes(keyword) ||
            query.pricepoint
              .toLowerCase()
              .includes(keyword) ||
            query.bio
              .toLowerCase()
              .includes(keyword)
          ) {
            this.searchedRestaurants.push(query);
            break;
          }
        }
      }
    }
    this.updateRestarants();
  }

  filterToggle() {
    var filters = document.getElementById('filters-mobile');

    if (filters.style.marginRight === "-400px") {
      filters.style.marginRight = "0px";
    } else {
      filters.style.marginRight = "-400px";
    }
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
