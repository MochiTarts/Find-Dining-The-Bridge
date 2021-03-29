import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RestaurantService } from '../../_services/restaurant.service';
import { SpinnerVisibilityService } from 'ng-http-loader';
import { cuisinesStr } from '../../_constants/cuisines';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { Title } from '@angular/platform-browser';
import { UserService } from '../../_services/user.service';
import { TokenStorageService } from '../../_services/token-storage.service';

@Component({
  selector: 'app-favourites',
  templateUrl: './favourites.component.html',
  styleUrls: ['./favourites.component.scss'],
})
export class FavouritesComponent implements OnInit {
  userId: string = '';
  role: string = '';
  restaurants: any[];
  emptyFavourites: boolean = true;

  allCuisines: any[];
  allRestaurants: any[];

  priceFilterRestaurants: any[];
  deliveryFilterRestaurants: any[];
  cuisineFilterRestaurants: any[];
  searchedRestaurants: any[];
  inputRestaurant: string = '';

  faSearch = faSearch;

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
    this.allCuisines = cuisinesStr;
    this.loadRestaurant(this.userId);
    this.titleService.setTitle("Favourites | Find Dining Scarborough");
  }

  loadRestaurant(userId: string): void {
    /* Replace this with method for calling list
       of favourite restaurants by userId */
    this.userService.getFavouriteRestaurants().subscribe((data) => {
      this.restaurants = data
      if (this.restaurants != undefined && this.restaurants.length != 0) {
        this.emptyFavourites = false
      }
      this.allRestaurants = this.restaurants
      this.priceFilterRestaurants = this.restaurants;
      this.deliveryFilterRestaurants = this.restaurants;
      this.cuisineFilterRestaurants = this.restaurants;
      this.searchedRestaurants = this.restaurants;
    })
  }

  updateRestarants() {
    this.restaurants = [];
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

  // This is for the enter key press on check boxes.
  filterEnter(event){
    event.srcElement.click();
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

}
