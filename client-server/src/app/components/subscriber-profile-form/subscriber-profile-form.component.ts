import { AfterViewInit, TemplateRef } from '@angular/core';
import { ViewChild } from '@angular/core';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';
import { UserService } from 'src/app/_services/user.service';
import { formValidator } from 'src/app/_validation/formValidator';
import { userValidator } from 'src/app/_validation/userValidator';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-subscriber-profile-form',
  templateUrl: './subscriber-profile-form.component.html',
  styleUrls: ['./subscriber-profile-form.component.scss'],
  exportAs: 'subscriberForm'
})
export class SubscriberProfileFormComponent implements OnInit {

  @ViewChild('userInfo', { static: true }) buContent: TemplateRef<any>;
  role: string = '';
  email: string = '';
  userId: string = '';
  username: string = '';
  profileId: string = '';
  userData: any;
  siteKey: string;
  loggedOut: boolean = true;
  closeButton: boolean = false;

  aFormGroup: FormGroup;
  validator: formValidator = new userValidator();
  modalRef: any;

  constructor(
    private modalService: NgbModal,
    private router: Router,
    private authService: AuthService,
    private tokenStorageService: TokenStorageService,
    private userService: UserService,
    private formBuilder: FormBuilder
  ) { }

  ngOnInit(): void { }

  open(closeButton: boolean): void {
    if (this.authService.isLoggedIn) {
      const user = this.tokenStorageService.getUser();
      this.role = user.role;
      this.username = user.username;
      this.email = user.email;
      this.userId = user.user_id;
      this.profileId = user.profile_id;

      this.siteKey = `${environment.captcha.siteKey}`;
      this.aFormGroup = this.formBuilder.group({
        recaptcha: ['', Validators.required],
        firstname: ['', Validators.required],
        lastname: ['', Validators.required],
        postalcode: ['', Validators.required],
        phone: ['', Validators.required],
        terms: ['', Validators.requiredTrue],
      });

      this.closeButton = closeButton;
      this.modalRef = this.modalService.open(this.buContent, { backdrop: 'static', keyboard: false });
    }
  }

  reload() {
    let currentUrl = this.router.url;
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate([currentUrl]);
  }

  updateProfile(): void {
    var sduserInfo = {
      email: this.email,
      profile_id: this.userId,
      first_name: (<HTMLInputElement>document.getElementById('firstname')).value,
      last_name: (<HTMLInputElement>document.getElementById('lastname')).value,
    }

    var subscriberInfo = {
      user_id: this.userId,
      postalCode: (<HTMLInputElement>document.getElementById('postalcode')).value,
      phone: <any>(<HTMLInputElement>document.getElementById('phone')).value,
    };

    if (this.profileId == '') {
      subscriberInfo["consent_status"] = ((<HTMLInputElement>document.getElementById('casl')).checked ? "EXPRESSED" : "IMPLIED");
    }

    // clear formErrors
    this.validator.clearAllErrors();
    //validate all formfields, the callback will throw appropriate errors, return true if any validation failed
    let failFlagOne = this.validator.validateAll(sduserInfo, (key) => this.validator.setError(key));
    let failFlagOneTwo = this.validator.validateAll(subscriberInfo, (key) => this.validator.setError(key));
    //if any validation failed, do not POST
    if (!failFlagOne && !failFlagOneTwo) {
      subscriberInfo.phone = Number(subscriberInfo.phone);
      /*
      Update sduser first_name, last_name
      Make new subscriber profile form with postalCode, phone, and consent_status if profile_id empty
      Otherwise, update existing subscriber profile if profile_id has value in it
      (Be sure to update the sduser record with the profile_id of the newly created subscriber profile)
      Call refresh token to get a new token with a profile_id that is no longer null
      */
      this.userService.editAccountUser(sduserInfo).subscribe(() => {
        /*
        Check if profile_id is null. If so, create subscriber profile
        If not, edit subscriber profile
        */
        if (this.profileId) {
          this.userService.editSubscriberProfile(subscriberInfo).subscribe(() => {
            alert("Updating subscriber profile");
            this.modalRef.close();
            this.reload();
          })
        } else {
          this.userService.createSubscriberProfile(subscriberInfo).subscribe(() => {
            alert("Creating new subscriber profile");
            // Call refresh token here
            this.modalRef.close();
            this.reload();
          })
        }
      })
    }
  }

}
