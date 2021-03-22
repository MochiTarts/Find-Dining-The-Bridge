import { Component, OnInit, ViewChild } from '@angular/core';
import { SubscriberProfileFormComponent } from 'src/app/components/subscriber-profile-form/subscriber-profile-form.component';
import { TokenStorageService } from '../../_services/token-storage.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  currentUser: any;
  @ViewChild('userInfo') userInfo: SubscriberProfileFormComponent;

  constructor(private token: TokenStorageService) { }

  ngOnInit(): void {
    this.currentUser = this.token.getUser();
    console.log(this.currentUser)
  }

  openEditModal(): void {
    this.userInfo.open(true);
  }

}