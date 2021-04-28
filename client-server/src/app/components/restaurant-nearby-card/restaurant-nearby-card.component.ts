import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';

@Component({
  selector: 'app-restaurant-nearby-card',
  templateUrl: './restaurant-nearby-card.component.html',
  styleUrls: ['./restaurant-nearby-card.component.scss']
})
export class RestaurantNearbyCardComponent implements OnInit {

  @Input() restaurant: any;

  constructor(
    private router: Router,
    private authService: AuthService,
    private tokenStorage: TokenStorageService,
  ) { }

  ngOnInit(): void {
  }

  gotoRestaurant() {
    const url = this.router.createUrlTree(['/restaurant'], { queryParams: { restaurantId: this.restaurant._id } });
    window.open(url.toString(), '_blank');
    // this.router.navigate(['/restaurant'], { queryParams: { restaurantId: this.restaurant._id } }).then(() => {
    //   this.reload();
    // })
  }

  reload() {
    this.authService.refreshToken().subscribe((token) => {
      this.tokenStorage.updateTokenAndUser(token.access);
      let currentUrl = this.router.url;
      this.router.routeReuseStrategy.shouldReuseRoute = () => false;
      this.router.onSameUrlNavigation = 'reload';
      this.router.navigate([currentUrl]);
    });
  }

}
