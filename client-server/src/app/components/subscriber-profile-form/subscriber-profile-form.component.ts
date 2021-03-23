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
  firstName: string = '';
  lastName: string = '';
  postalCode: string = '';
  phone: string = '';
  siteKey: string;
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

  ngOnInit(): void {
    if (this.authService.isLoggedIn) {
      const user = this.tokenStorageService.getUser();
      this.role = user.role;
      this.email = user.email;
      this.username = user.username;
      this.email = user.email;
      this.userId = user.user_id;
      this.profileId = user.profile_id;

      if (this.userId) {
        this.userService.getSubscriberProfile(this.userId).subscribe((data) => {
          this.firstName = data.first_name;
          this.lastName = data.last_name;
          this.postalCode = data.postalCode;
          this.phone = data.phone;
          console.log(this.firstName)
        })
      }
    }
  }

  open(closeButton: boolean): void {
    if (this.authService.isLoggedIn) {
      this.siteKey = `${environment.captcha.siteKey}`;
      if (!this.closeButton) {
        this.aFormGroup = this.formBuilder.group({
          recaptcha: ['', Validators.required],
          firstname: ['', Validators.required],
          lastname: ['', Validators.required],
          postalcode: ['', Validators.required],
          phone: ['', Validators.required],
          terms: ['', Validators.requiredTrue],
        });
      } else {
        this.aFormGroup = this.formBuilder.group({
          recaptcha: ['', Validators.required],
          firstname: ['', Validators.required],
          lastname: ['', Validators.required],
          postalcode: ['', Validators.required],
          phone: ['', Validators.required],
        });
      }

      this.aFormGroup.get('firstname').setValue(String(this.firstName));
      this.aFormGroup.get('lastname').setValue(String(this.lastName));
      this.aFormGroup.get('postalcode').setValue(String(this.postalCode));
      this.aFormGroup.get('phone').setValue(String(this.phone));

      this.closeButton = closeButton;
      this.modalRef = this.modalService.open(this.buContent, { backdrop: 'static', keyboard: false });
    }
  }

  updateProfile(): void {
    var sduserInfo = {
      email: this.email,
      profile_id: this.userId,
    };

    var subscriberInfo = {
      user_id: this.userId,
      first_name: (<HTMLInputElement>document.getElementById('firstname')).value,
      last_name: (<HTMLInputElement>document.getElementById('lastname')).value,
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
      */
      this.userService.editAccountUser(sduserInfo).subscribe(() => {
        /*
        Check if profile_id is null. If so, create subscriber profile
        If not, edit subscriber profile
        */
        if (this.profileId) {
          this.userService.editSubscriberProfile(subscriberInfo).subscribe(() => {
            this.modalRef.close();
            this.reload();
          })
        } else {
          this.userService.createSubscriberProfile(subscriberInfo).subscribe(() => {
            this.authService.refreshToken().subscribe((token) => {
              this.tokenStorageService.updateTokenAndUser(token.access);
              this.modalRef.close();
              this.reload();
            })
          })
        }
      })
    }
  }

  reload() {
    let currentUrl = this.router.url;
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate([currentUrl]);
  }

}
