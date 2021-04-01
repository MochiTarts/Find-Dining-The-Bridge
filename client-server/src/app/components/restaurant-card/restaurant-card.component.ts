import { Component, OnInit, Input, OnChanges, SimpleChanges } from '@angular/core';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';

@Component({
  selector: 'app-restaurant-card',
  templateUrl: './restaurant-card.component.html',
  styleUrls: ['./restaurant-card.component.scss'],
})
export class RestaurantCardComponent implements OnInit, OnChanges {
  @Input() restaurant: any;
  @Input() favList: any;

  favourited: boolean = false;
  userId: string = '';
  role: string = '';
  cuisineList: string = '';
  pricepoints: any = [];
  pricepoint: string = '';
  serviceList: string = '';

  constructor(
    private userService: UserService,
    private tokenStorage: TokenStorageService,
  ) {}

  ngOnInit(): void {
    var user = this.tokenStorage.getUser();
      this.userId = user.user_id
      this.role = user.role

      this.pricepoints = [
        {key: "$", value: "LOW"},
        {key: "$$", value: "MID"},
        {key: "$$$", value: "HIGH"},
        {key: "$$$$", value: "EXHIGH"}
      ]

      for (let cuisine of this.restaurant.cuisines) {
        if (this.cuisineList == '') {
          this.cuisineList = String(cuisine);
        } else {
          this.cuisineList = this.cuisineList + ", " + String(cuisine);
        }
      }

      let price = String(this.restaurant.pricepoint);
      for (let p of this.pricepoints) {
        if (p["value"] == price) {
          this.pricepoint = p["key"];
        }
      }

      for (let service of this.restaurant.offer_options) {
        if (this.serviceList == '') {
          this.serviceList = String(service);
        } else {
          this.serviceList = this.serviceList + " | " + String(service);
        }
      }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['favList']) {
      for (let fav of this.favList) {
        if (fav._id == this.restaurant._id) {
          this.favourited = true;
          break;
        } else {
          this.favourited = false;
        }
      }
    }
  }

  addFavourite(restaurnt_id) {
    var data = {
      restaurant: restaurnt_id
    }
    this.userService.addFavouriteRestaurant(data).subscribe(() => {
      this.favourited = true
      this.favList.push(this.restaurant);
    },(error) => {
      alert(error.error.message)
    })
  }

}
