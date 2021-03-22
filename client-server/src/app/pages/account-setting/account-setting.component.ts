import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { UserService } from '../../_services/user.service';
import { AuthService } from '../../_services/auth.service';
import { Router } from "@angular/router";
import { Title } from '@angular/platform-browser';
import { TokenStorageService } from '../../_services/token-storage.service';

@Component({
  selector: 'app-account-setting',
  templateUrl: './account-setting.component.html',
  styleUrls: ['./account-setting.component.scss']
})
export class AccountSettingComponent implements OnInit {
  modalRef: any;
  userId: string;
  idToken: string = '';

  constructor(
    private modalService: NgbModal,
    private userService: UserService,
    private tokenStorage: TokenStorageService,
    public authService: AuthService,
    public router: Router,
    private titleService: Title 
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Account Settings | Find Dining Scarborough");
  }

  openConfirmModal(content) {
    this.modalRef = this.modalService.open(content, { backdrop: 'static', keyboard: false });
  }

  deactivateAccount() {
    var user = this.tokenStorage.getUser();
    this.userService.deactivateUser(user.user_id).subscribe(data => {
      this.modalRef.close();
      this.reload()
      this.tokenStorage.signOut();
      this.authService.updateLoginStatus(false);
      this.router.navigate(['/'])
    }, err => {
      console.log(err);
    });
    
  }

  reload() {
    let currentUrl = this.router.url;
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate([currentUrl]);
  }

}