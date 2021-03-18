import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-restaurant-nearby-card',
  templateUrl: './restaurant-nearby-card.component.html',
  styleUrls: ['./restaurant-nearby-card.component.scss']
})
export class RestaurantNearbyCardComponent implements OnInit {

  @Input() restaurant: any;

  constructor() { }

  ngOnInit(): void {
  }

}
