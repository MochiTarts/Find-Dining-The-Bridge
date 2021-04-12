import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';
import { UserService } from 'src/app/_services/user.service';
import { RestaurantService } from 'src/app/_services/restaurant.service';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-newsletter',
  templateUrl: './newsletter.component.html',
  styleUrls: ['./newsletter.component.scss']
})
export class NewsletterComponent implements OnInit {
  userId: string = '';
  role: string = '';
  subscribed: boolean = false;
  unsubscribed: boolean = false;

  constructor(
    private userService: UserService,
    private restaurantService: RestaurantService,
    private router: Router,
    private authService: AuthService,
    private tokenStorageService: TokenStorageService,
    private titleService: Title,
  ) { }

  ngOnInit(): void {
    const user = this.tokenStorageService.getUser();
    this.userId = user.user_id;
    this.role = user.role;

    this.subscribed = false;
    this.unsubscribed = false;
  }

  subscribeNewsletter() {
    this.titleService.setTitle("Newsletter | Find Dining Scarborough");
    var userInfo = {
      consent_status: "EXPRESSED"
    }
    if (this.role == 'BU') {
      this.userService.editSubscriberProfile(userInfo).subscribe(() => {
        this.subscribed = true;
        alert("You have successfully subscribed! You will now receive emails regarding important about Find Dining or Restaurant promotions.");
        this.reload();
      });
    } else if (this.role == 'RO') {
      this.restaurantService.roEdit(userInfo).subscribe(() => {
        this.subscribed = true;
        alert("You have successfully subscribed! You will now receive emails regarding important about Find Dining or Restaurant promotions.");
        this.reload();
      })
    } else {
      alert("Your role is neither RO nor BU");
    }
  }

  unsubscribeNewsletter() {
    var userInfo = {
      consent_status: "UNSUBSCRIBED",
    }
    if (this.role == 'BU') {
      this.userService.editSubscriberProfile(userInfo).subscribe(() => {
        this.unsubscribed = true;
        alert("You have successfully unsubscribed.");
        this.reload();
      });
    } else if (this.role == 'RO') {
      this.restaurantService.roEdit(userInfo).subscribe(() => {
        this.subscribed = true;
        alert("You have successfully subscribed! You will now receive emails regarding important about Find Dining or Restaurant promotions.");
        this.reload();
      })
    } else {
      alert("Your role is neither RO nor BU");
    }
  }

  reload() {
    this.authService.refreshToken().subscribe((token) => {
      this.tokenStorageService.updateTokenAndUser(token.access);
      this.router.navigate(['']);
    })
  }

}
