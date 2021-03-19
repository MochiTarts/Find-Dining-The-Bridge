import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';

@Component({
  selector: 'app-restaurant-favs-card',
  templateUrl: './restaurant-favs-card.component.html',
  styleUrls: ['./restaurant-favs-card.component.scss']
})
export class RestaurantFavsCardComponent implements OnInit {
  @Input() restaurant: any;

  userId: string = '';
  role: string = '';
  cuisineList: string = '';
  pricepoints: any = [];
  pricepoint: string = '';
  serviceList: string = '';
  totalStars = 5;

  constructor(
    private userService: UserService,
    private router: Router,
    private tokenStorage: TokenStorageService,
  ) { }

  ngOnInit(): void {
    var user = this.tokenStorage.getUser();
    this.userId = user.email;
    this.role = user.role;

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

  reload() {
    let currentUrl = this.router.url;
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate([currentUrl]);
  }

  remove(restaurnt_id) {
    var data = {
      user: this.userId,
      restaurant: restaurnt_id
    }
    this.userService.removeFavRestaurant(data).subscribe(() => {
      this.reload()
    },(error) => {
      alert(error.error.message)
    })
  }

}