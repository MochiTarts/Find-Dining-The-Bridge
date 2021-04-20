import { Component, OnInit, ViewChild } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { UserService } from '../../_services/user.service';
import { AuthService } from '../../_services/auth.service';
import { Router } from "@angular/router";
import { Title } from '@angular/platform-browser';
import { TokenStorageService } from '../../_services/token-storage.service';
import { PasswordChangeFormComponent } from '../../components/password-change-form/password-change-form.component';

@Component({
  selector: 'app-account-setting',
  templateUrl: './account-setting.component.html',
  styleUrls: ['./account-setting.component.scss']
})
export class AccountSettingComponent implements OnInit {
  modalRef: any;
  userId: string = '';
  profileId: string = '';
  role: string = '';
  isThirdParty: boolean = false;
  @ViewChild('changePassword') changePassword: PasswordChangeFormComponent;
  
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
    if (this.tokenStorage.getProvider()){
      this.isThirdParty = true;
    }

    this.userId = this.tokenStorage.getUser().user_id;
    this.role = this.tokenStorage.getUser().role;
    this.profileId = this.tokenStorage.getUser().profile_id;

    if (!this.profileId) {
      if (this.role == 'BU') {
        // Will open profile modal on home page
        this.router.navigate(['/']);
        return;
      } else {
        this.router.navigate(['/restaurant-setup']);
        return;
      }
    }
  }

  /**
   * Opens the modal asking for confirmation on account deactivation
   * @param content - the modal to open
   */
  openConfirmModal(content) {
    this.modalRef = this.modalService.open(content, { backdrop: 'static', keyboard: false });
  }

  /**
   * Performs action to deactivate the current user
   */
  deactivateAccount() {
    var user = this.tokenStorage.getUser();
    this.userService.deactivateUser(user.user_id).subscribe(data => {
      this.modalRef.close();
      this.reload();
      this.tokenStorage.signOut();
      this.authService.updateLoginStatus(false);
      this.router.navigate(['']);
    }, err => {
      alert(err.error.message);
      // fail to send email but account is successfully deactivated
      if (err.error.code == 'fail_to_send_email'){
        this.modalRef.close();
        this.reload();
        this.tokenStorage.signOut();
        this.authService.updateLoginStatus(false);
        this.router.navigate(['']);
      }
      // console.log(err);
    });

  }

  reload() {
    let currentUrl = this.router.url;
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate([currentUrl]);
  }

}
