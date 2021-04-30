import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RestaurantService } from '../../_services/restaurant.service';
import { SpinnerVisibilityService } from 'ng-http-loader';
import { cuisinesStr } from '../../_constants/cuisines';
import { servicesStr } from '../../_constants/services';
import { faSearch, faArrowCircleLeft, } from '@fortawesome/free-solid-svg-icons';
import { Title } from '@angular/platform-browser';
import { UserService } from '../../_services/user.service';
import { TokenStorageService } from '../../_services/token-storage.service';
import { Observable, OperatorFunction } from 'rxjs';
import {debounceTime, distinctUntilChanged, map} from 'rxjs/operators';


var searchItems = [];

@Component({
  selector: 'app-favourites',
  templateUrl: './favourites.component.html',
  styleUrls: ['./favourites.component.scss'],
})
export class FavouritesComponent implements OnInit {
  userId: string = '';
  role: string = '';
  profileId: string = '';
  restaurants: any[];
  emptyFavourites: boolean = true;

  allCuisines: any[];
  allServices: any[];
  allRestaurants: any[];

  priceFilterRestaurants: any[];
  deliveryFilterRestaurants: any[];
  cuisineFilterRestaurants: any[];
  serviceFilterRestaurants: any[];
  searchedRestaurants: any[];
  inputRestaurant: string = '';

  faSearch = faSearch;
  faArrowCircleLeft = faArrowCircleLeft;
  show: number = 3;

  constructor(
    private restaurantService: RestaurantService,
    private userService: UserService,
    private tokenStorage: TokenStorageService,
    private route: ActivatedRoute,
    private router: Router,
    private spinner: SpinnerVisibilityService,
    private titleService: Title,
  ) { }

  ngOnInit(): void {
    var user = this.tokenStorage.getUser();
    this.userId = user.user_id;
    this.role = user.role;
    this.profileId = user.profile_id;

    if (!this.profileId) {
      if (this.role == 'BU') {
        // Will open profile modal on home page
        this.router.navigate(['/']);
        return;
      } else {
        this.router.navigate(['/restaurant-setup']);
        return;
      }
    }

    this.allCuisines = cuisinesStr;
    this.allServices = servicesStr;
    this.loadRestaurant(this.userId);
    this.titleService.setTitle("Favourites | Find Dining Scarborough");
  }

  /**
   * Retrieves the list of favourited restaurants by the user
   * @param userId - the user's user_id
   */
  loadRestaurant(userId: string): void {
    /* Replace this with method for calling list
       of favourite restaurants by userId */
    this.userService.getFavouriteRestaurants().subscribe((data) => {
      this.restaurants = data;
      searchItems = data.map(function(a) {return {name: a['name'], image: a['logo_url']}});
      searchItems = searchItems.concat(
        cuisinesStr.map(function(a) {return {name: a}}),
        servicesStr.map(function(a) {return {name: a}}));
      if (this.restaurants != undefined && this.restaurants.length != 0) {
        this.emptyFavourites = false
      }
      this.allRestaurants = this.restaurants
      this.priceFilterRestaurants = this.restaurants;
      this.deliveryFilterRestaurants = this.restaurants;
      this.cuisineFilterRestaurants = this.restaurants;
      this.serviceFilterRestaurants = this.restaurants;
      this.searchedRestaurants = this.restaurants;
    })
  }

  /**
   * Updates the list of favourited restaurants to be displayed
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
   * Updates the list of searchedRestaurants based on search
   * criteria
   */
  searchRestaurants() {
    if (this.inputRestaurant == '') {
      this.searchedRestaurants = this.allRestaurants;
    } else {
      this.searchedRestaurants = [];
      let keywords = this.inputRestaurant.toLowerCase().replace(/\,/gi, ' ').split(' ');
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

  /**
   * Clicks the checkbox on enter key
   * @param event - the event that triggers this function
   */
  filterEnter(event) {
    event.srcElement.click();
  }

  /**
   * Updates the cuisineFilterRestaurants list based on the selected cuisines. Then updates
   * the list of favourited restaurants to display
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
   * the list of favourited restaurants to display
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

  /**
   * Updates the priceFilterRestaurants list based on the selected pricepoints. Then updates
   * the list of favourited restaurants to display
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

  filterToggle() {
    var filters = document.getElementById('filters-mobile');

    if (filters.style.marginRight === "-400px") {
      filters.style.marginRight = "0px";
    } else {
      filters.style.marginRight = "-400px";
    }
  }

  /**
   * Redirects to the all-listings page
   */
  goBack() {
    this.router.navigate(['/all-listings']);
  }

  formatter = (x) => x.hasOwnProperty('name') ? x.name : x;
  search: OperatorFunction<string, readonly string[]> = (text$: Observable<string>) =>
    text$.pipe(
      debounceTime(200),
      distinctUntilChanged(),
      map(term => term.length < 1 ? []
        : searchItems.filter(v => v.name.toLowerCase().indexOf(term.toLowerCase()) == 0).
          concat(searchItems.filter(v => v.name.toLowerCase().indexOf(term.toLowerCase()) > 0)).slice(0, 10))
    )

}
