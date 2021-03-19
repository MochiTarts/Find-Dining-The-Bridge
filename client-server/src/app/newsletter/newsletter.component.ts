import { Component, OnInit } from '@angular/core';
import { UserService } from 'src/app/_services/user.service';

@Component({
  selector: 'app-newsletter',
  templateUrl: './newsletter.component.html',
  styleUrls: ['./newsletter.component.scss']
})
export class NewsletterComponent implements OnInit {
  subscribed: boolean = false;
  unsubscribed: boolean = false;

  constructor(
    private userService: UserService,
  ) { }

  ngOnInit(): void {
    this.subscribed = false;
    this.unsubscribed = false;
  }

  subscribeNewsletter() {
    var userInfo = {
      email: (<HTMLInputElement>document.getElementById('email')).value,
      consent_status: "EXPRESSED"
    }
    this.userService.editConsentStatus(userInfo);
    this.subscribed = true;
  }

  unsubscribeNewsletter() {
    var userInfo = {
      email: (<HTMLInputElement>document.getElementById('email')).value,
      consent_status: "UNSUBSCRIBED",
    }
    this.userService.editConsentStatus(userInfo);
    this.unsubscribed = true;
  }
}
