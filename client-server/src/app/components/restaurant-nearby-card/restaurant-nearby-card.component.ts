import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-restaurant-nearby-card',
  templateUrl: './restaurant-nearby-card.component.html',
  styleUrls: ['./restaurant-nearby-card.component.scss']
})
export class RestaurantNearbyCardComponent implements OnInit {

  @Input() restaurant: any;

  constructor(
    private router: Router,
  ) { }

  ngOnInit(): void {
  }

  gotoRestaurant() {
    const url = this.router.createUrlTree(['/restaurant'], { queryParams: { restaurantId: this.restaurant._id } });
    window.open(url.toString(), '_self');
  }

}
