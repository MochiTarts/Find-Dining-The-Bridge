import { Component, OnInit, Input } from '@angular/core';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { RestaurantService } from '../../_services/restaurant.service';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from '../../_services/token-storage.service';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.scss']
})
export class PostComponent implements OnInit {
  @Input() role: string;
  @Input() id: string;
  @Input() post: any;

  currentUser: any = {};

  postId: string = '';
  userId: string = '';
  restaurantId: string = '';
  isQueryRestaurant: boolean = false;

  deleteModalRef: any;

  faTrash = faTrash;

  constructor(
    private restaurantService: RestaurantService,
    private route: ActivatedRoute,
    private authService: AuthService,
    private tokenStorage: TokenStorageService,
  ) { }

  ngOnInit(): void {
    if (this.authService.isLoggedIn) {
      const user = this.tokenStorage.getUser();
      this.role = user.role;
      this.userId = user.user_id;
    }

    this.restaurantId = this.route.snapshot.queryParams.restaurantId || this.userId;

    if (this.restaurantId == this.route.snapshot.queryParams.restaurantId) this.isQueryRestaurant = true;

    this.getPendingOrApproved(this.restaurantId).subscribe((data) => {
      this.post.restaurant_name = data.name;
    })
  }

  getPendingOrApproved(id) {
    if (this.authService.isLoggedIn && this.role == 'RO' && !this.isQueryRestaurant) {
      return this.restaurantService.getPendingRestaurant();
    } else {
      return this.restaurantService.getApprovedRestaurant(id);
    }
  }

}
