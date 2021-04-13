import { ChangeDetectorRef, Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { FormGroup, FormControl, FormBuilder, Validators } from '@angular/forms';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { UserService } from 'src/app/_services/user.service';
import { formValidator } from 'src/app/_validation/formValidator';
import { passwordValidator } from 'src/app/_validation/passwordValidator';

@Component({
  selector: 'app-password-change-form',
  templateUrl: './password-change-form.component.html',
  styleUrls: ['./password-change-form.component.scss']
})
export class PasswordChangeFormComponent implements OnInit {

  @ViewChild('changePassword', { static: true }) passwordContent: TemplateRef<any>;

  modalRef: any;
  aFormGroup: FormGroup;
  validator: formValidator = new passwordValidator();
  strength: number = 0;
  showDetails: boolean = true;
  closeButton: boolean = false;

  constructor(
    private formBuilder: FormBuilder,
    private ref: ChangeDetectorRef,
    private modalService: NgbModal,
    private userService: UserService) { }

  ngOnInit(): void {
  }


  /**
   * Opens the change password modal
   * @param closeButton - determines if the close button should be displayed on the modal
   */
  open(closeButton: boolean): void {
    this.aFormGroup = this.formBuilder.group({
      oldPassword: ['', Validators.required],
      newPassword: ['', Validators.required],
      confirmPassword: ['', Validators.required],
    });
    this.closeButton = closeButton;
    this.modalRef = this.modalService.open(this.passwordContent, { backdrop: 'static', keyboard: false });
  }

  /**
   * Performs action to let a user change their password
   */
  changeUserPassword(): void {
    var passwords = {
      old_password: (<HTMLInputElement>document.getElementById('oldPassword')).value,
      new_password1: (<HTMLInputElement>document.getElementById('newPassword')).value,
      new_password2: (<HTMLInputElement>document.getElementById('confirmPassword')).value,
    };

    this.userService.changeUserPassword(passwords).subscribe((data)=>{
      console.log(data);
    },
    err => {
      console.log(err);

      var errors = err.error,
      old_password_error = errors.old_password,
      new_password1_error = errors.new_password1,
      new_password2_error = errors.new_password2;

      // incorrect old password
      if (old_password_error){
        console.log(old_password_error[0].message);
      }
      // old password equals the new password
      if (new_password1_error){
        console.log(new_password1_error[0].message);
      }
      // new passwords don't match
      if (new_password2_error){
        console.log(new_password2_error[0].message);
      }
    });

    // clear formErrors
    this.validator.clearAllErrors();

  }


  onStrengthChanged(strength: number) {
    this.strength = strength;
  }

}
