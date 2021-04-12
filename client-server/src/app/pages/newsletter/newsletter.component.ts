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

  constructor(
    private userService: UserService,
    private restaurantService: RestaurantService,
    private router: Router,
    private authService: AuthService,
    private tokenStorageService: TokenStorageService,
    private titleService: Title,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Newsletter | Find Dining Scarborough");
    const user = this.tokenStorageService.getUser();
    this.userId = user.user_id;
    this.role = user.role;

    this.subscribed = false;

    this.chooseGetAPI().subscribe((data) => {
      this.subscribed = (data.consent_status == "EXPRESSED");
    });
  }

  subscribeNewsletter() {
    var userInfo = {
      consent_status: "EXPRESSED"
    }
    this.chooseEditAPI(userInfo).subscribe(() => {
      this.subscribed = true;
      alert("You have successfully subscribed! You will now receive emails regarding important about Find Dining or Restaurant promotions.");
      this.reload();
    });
  }

  unsubscribeNewsletter() {
    var userInfo = {
      consent_status: "UNSUBSCRIBED",
    }
    this.chooseEditAPI(userInfo).subscribe(() => {
      this.subscribed = false;
      alert("You have successfully unsubscribed.");
      this.reload();
    });
  }

  chooseEditAPI(userInfo) {
    if (this.role == 'BU') {
      return this.userService.editSubscriberProfile(userInfo);
    } else if (this.role == 'RO') {
      return this.restaurantService.roEdit(userInfo);
    }
  }

  chooseGetAPI() {
    if (this.role == 'BU') {
      return this.userService.getSubscriberProfile();
    } else if (this.role == 'RO') {
      return this.restaurantService.roGet();
    }
  }

  reload() {
    this.authService.refreshToken().subscribe((token) => {
      this.tokenStorageService.updateTokenAndUser(token.access);
      this.router.navigate(['']);
    })
  }

}
