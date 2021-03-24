import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';
import { UserService } from 'src/app/_services/user.service';

@Component({
  selector: 'app-newsletter',
  templateUrl: './newsletter.component.html',
  styleUrls: ['./newsletter.component.scss']
})
export class NewsletterComponent implements OnInit {
  userId: string = '';
  subscribed: boolean = false;
  unsubscribed: boolean = false;

  constructor(
    private userService: UserService,
    private router: Router,
    private authService: AuthService,
    private tokenStorageService: TokenStorageService,
  ) { }

  ngOnInit(): void {
    const user = this.tokenStorageService.getUser();
    this.userId = user.user_id;

    this.subscribed = false;
    this.unsubscribed = false;
  }

  subscribeNewsletter() {
    var userInfo = {
      user_id: this.userId,
      consent_status: "EXPRESSED"
    }
    this.userService.editConsentStatus(userInfo).subscribe(() => {
      this.subscribed = true;
      alert("You have successfully subscribed! You will now receive emails regarding important about Find Dining or Restaurant promotions.");
      this.reload();
    });
  }

  unsubscribeNewsletter() {
    var userInfo = {
      user_id: this.userId,
      consent_status: "UNSUBSCRIBED",
    }
    this.userService.editConsentStatus(userInfo).subscribe(() => {
      this.unsubscribed = true;
      alert("You have successfully unsubscribed.");
      this.reload();
    });
  }

  reload() {
    this.authService.refreshToken().subscribe((token) => {
      this.tokenStorageService.updateTokenAndUser(token.access);
      this.router.navigate(['']);
    })
  }

}
