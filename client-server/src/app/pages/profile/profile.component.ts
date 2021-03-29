import { Component, OnInit, ViewChild } from '@angular/core';
import { SubscriberProfileFormComponent } from 'src/app/components/subscriber-profile-form/subscriber-profile-form.component';
import { UserService } from 'src/app/_services/user.service';
import { TokenStorageService } from '../../_services/token-storage.service';
import { Router } from '@angular/router';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  currentUser: any = {};
  @ViewChild('userInfo') userInfo: SubscriberProfileFormComponent;

  constructor(
    private token: TokenStorageService,
    private userService: UserService,
    private router: Router,
    private titleService: Title,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Profile | Find Dining Scarborough");
    this.currentUser = this.token.getUser();
    this.userService.getSubscriberProfile().subscribe((data) => {
      this.currentUser.first_name = data.first_name;
      this.currentUser.last_name = data.last_name;
      this.currentUser.postalCode = data.postalCode;
      var phone: string = String(data.phone);
      this.currentUser.phone = phone != 'null' ? "(" + phone.slice(0, 3) + ") " + phone.slice(3, 6) + " " + phone.slice(6, 10) : '';
    },
      err => {
        console.log(err);
        if (err.error && err.error.code == 'no_profile_found') {
          // redirect to home page to fill the profile
          this.router.navigate(['/']);
        }
      })
  }

  openEditModal(): void {
    this.userInfo.open(true);
  }

}
