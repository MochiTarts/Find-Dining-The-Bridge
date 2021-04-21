import { AfterViewInit, TemplateRef } from '@angular/core';
import { ViewChild } from '@angular/core';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';
import { UserService } from 'src/app/_services/user.service';
import { formValidation } from 'src/app/_validation/forms';
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

      if (this.role == 'BU' && this.profileId) {
        this.userService.getSubscriberProfile().subscribe((data) => {
          this.firstName = data.first_name;
          this.lastName = data.last_name;
          this.postalCode = data.postalCode;
          this.phone = data.phone;
        },
          err => {
            if (err.error && err.error.code == 'no_profile_found') {
              // redirect to home page to fill the profile
              this.router.navigate(['/']);
            }
          })
      }
    }
  }

  /**
   * Opens the modal for user profile form
   * @param closeButton - determines if the close button should be displayed on the modal
   */
  open(closeButton: boolean): void {
    if (this.authService.isLoggedIn) {
      this.siteKey = `${environment.captcha.siteKey}`;
      if (!closeButton) {
        this.aFormGroup = this.formBuilder.group({
          recaptcha: ['', Validators.required],
          firstname: [''],
          lastname: [''],
          postalcode: [''],
          phone: [''],
          terms: ['', Validators.requiredTrue],
        });
      } else {
        this.aFormGroup = this.formBuilder.group({
          recaptcha: ['', Validators.required],
          firstname: [''],
          lastname: [''],
          postalcode: [''],
          phone: [''],
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

  addFieldsForProfanityCheck(profile) {
    let newProfile = Object.assign({}, profile);
    newProfile['first_name_p'] = profile.first_name;
    newProfile['last_name_p'] = profile.last_name;
    return newProfile;
  }

  /**
   * Performs action to update or create the user's profile
   */
  updateProfile(): void {
    var subscriberInfo = {
      first_name: (<HTMLInputElement>document.getElementById('firstname')).value,
      last_name: (<HTMLInputElement>document.getElementById('lastname')).value,
      postalCode: (<HTMLInputElement>document.getElementById('postalcode')).value,
      phone: <any>(<HTMLInputElement>document.getElementById('phone')).value,
    };

    let profileForProfanityCheck = this.addFieldsForProfanityCheck(subscriberInfo);

    if (!this.profileId) {
      subscriberInfo["consent_status"] = ((<HTMLInputElement>document.getElementById('casl')).checked ? "EXPRESSED" : "IMPLIED")
    }

    // clear formErrors
    this.validator.clearAllErrors();
    //validate all formfields, the callback will throw appropriate errors, return true if any validation failed
    let failFlagOneTwo = this.validator.validateAll(profileForProfanityCheck, (key) => this.validator.setError(key));
    //if any validation failed, do not POST
    if (!failFlagOneTwo) {
      subscriberInfo.phone = Number(subscriberInfo.phone);
      /*
      Make new subscriber profile form with postalCode, phone, and consent_status if profile_id empty
      Otherwise, update existing subscriber profile if profile_id has value in it
      Updates sduser profile_id with id of newly created profile, if profile_id is currently null
      */

      if (this.profileId) {
        this.userService.editSubscriberProfile(subscriberInfo).subscribe(() => {
          this.modalRef.close();
          this.reload();
        },
          (error) => {
            if (formValidation.isInvalidResponse(error.error.detail)) {
              formValidation.HandleInvalid(error.error.detail, (key) => this.validator.setError(key));
            }
          })
      } else {
        this.userService.createSubscriberProfile(subscriberInfo).subscribe((profile) => {
          var sduserInfo = {
            profile_id: profile.id,
          };

          this.userService.editAccountUser(sduserInfo).subscribe(() => {
            this.authService.refreshToken().subscribe((token) => {
              this.tokenStorageService.updateTokenAndUser(token.access);
              this.modalRef.close();
              setTimeout(() => {
                this.reload();
              }, 100);
            })
          })
        },
          (error) => {
            if (formValidation.isInvalidResponse(error.error.detail)) {
              formValidation.HandleInvalid(error.error.detail, (key) => this.validator.setError(key));
            }
          })
      }
    }
  }

  reload() {
    window.location.reload();
  }

}
