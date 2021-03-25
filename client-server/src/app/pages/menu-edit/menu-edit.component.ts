import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';
import { RestaurantService } from '../../_services/restaurant.service';
import { formValidation } from '../../_validation/forms';
import { dishValidator } from '../../_validation/dishValidator';
import { formValidator } from '../../_validation/formValidator';
import { Title } from '@angular/platform-browser';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from '../../_services/token-storage.service';

@Component({
  selector: 'app-menu-edit',
  templateUrl: './menu-edit.component.html',
  styleUrls: ['./menu-edit.component.scss']
})
export class MenuEditComponent implements OnInit {
  restaurantId: string = '';
  userId: string = '';
  role: string = '';

  uploadForm: FormGroup;
  validator: formValidator = new dishValidator();
  newImage: boolean = false;

  faEdit = faEdit;
  faTrash = faTrash;

  deleteModalRef: any;
  dishModalRef: any;
  dishEdit: boolean = false;
  dishes: any[];
  dishIndex: number;

  dishId: string = '';
  dishName: string = '';
  price: string = '';
  menuCategory: string = '';
  description: string = '';

  showAlert: boolean = false;
  alertMessage: string = '';

  constructor(
    private router: Router,
    private formBuilder: FormBuilder,
    private restaurantsService: RestaurantService,
    private dishModalService: NgbModal,
    private deleteModalService: NgbModal,
    private titleService: Title,
    private authService: AuthService,
    private tokenStorage: TokenStorageService,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Edit Menu | Find Dining Scarborough");

    if (this.authService.isLoggedIn) {
      const user = this.tokenStorage.getUser();
      this.role = user.role;
      this.userId = user.user_id;
      this.restaurantId = user.profile_id;
    }

    // if (!this.restaurantId || this.role !== 'RO' || !this.userId) {
    //   this.router.navigate(['']);
    //   alert('No matching restaurant found for this profile!');
    // }
    this.loadAllDishes();

    this.uploadForm = this.formBuilder.group({
      file: [''],
    });
  }

  loadAllDishes() {
    this.restaurantsService.getPendingRestaurantFood().subscribe((data) => {
      this.dishes = data.Dishes;
    })
  }

  clearInput() {
    this.dishId = '';
    this.dishName = '';
    this.price = '';
    this.menuCategory = '';
    this.description = '';
  }

  openDishModal(content, dish?, index?) {
    if (dish !== undefined) {
      // dish edit
      this.dishId = dish._id;
      this.dishName = dish.name;
      this.price = dish.price;
      this.menuCategory = dish.category;
      this.description = dish.description;

      this.dishEdit = true;
      this.dishIndex = index;
    } else {
      this.clearInput();
    }

    // Reset alert
    this.showAlert = false;
    this.alertMessage = '';

    this.dishModalRef = this.dishModalService.open(content, { size: 'xl' });
  }

  openDeleteModal(content, dish, index) {
    this.dishName = dish.name;
    this.dishIndex = index;
    this.menuCategory = dish.category;
    this.deleteModalRef = this.deleteModalService.open(content, { size: 's' });
  }

  configDish() {
    // only used for form validation
    var validationInfo = {
      name: this.dishName,
      price: this.price,
      menuCategory: this.menuCategory,
      description: this.description,
    };

    this.validator.clearAllErrors();
    let failFlag = this.validator.validateAll(validationInfo, (key) =>
      this.validator.setError(key)
    );

    if (!failFlag) {
      const price: number = +this.price;
      var dishInfo = {
        name: this.dishName,
        description: this.description,
        price: price.toFixed(2),
        specials: '',
        category: this.menuCategory,
      };

      if (this.dishEdit) {
        this.restaurantsService.editPendingDish(dishInfo, this.dishId).subscribe((data) => {
          if (this.newImage) {
            this.onSubmit(data._id);
          } else {
            this.dishes[this.dishIndex] = data;
            this.dishIndex = 0;
            this.dishEdit = false;
          }
        },
        (error) => {
          this.alertMessage = error.error.message;
          this.showAlert = true;
        });
      } else {
        dishInfo['picture'] = '';
        this.restaurantsService.createPendingDish(dishInfo).subscribe((data) => {
          if (this.newImage) {
            this.onSubmit(data._id);
          } else {
            this.dishes.push(data);
          }
        },
        (error) => {
          this.alertMessage = error.error.message;
          this.showAlert = true;
        });
      }

      this.clearInput();
      this.dishModalRef.close();
    }
  }

  deleteDish() {
    var dishInfo = {
      name: this.dishName,
      category: this.menuCategory,
    };

    this.restaurantsService.deleteDish(dishInfo);

    if (this.dishIndex > -1) {
      this.dishes.splice(this.dishIndex, 1);
    }

    this.clearInput();
    this.dishIndex = 0;
    this.deleteModalRef.close();
  }

  back() {
    this.router.navigate(['/restaurant']);
  }

  onFileSelect(event) {
    if (event.target.files.length > 0) {
      this.newImage = true;
      const file = event.target.files[0];
      this.uploadForm.get('file').setValue(file);
    }
  }

  onSubmit(id: string) {
    // const formData = new FormData();
    // formData.append('file', this.uploadForm.get('file').value);
    // this.restaurantsService.uploadFoodMedia(formData, id).subscribe((data) => {
    //   if (this.dishEdit) {
    //     this.dishes[this.dishIndex] = data;
    //     this.dishIndex = 0;
    //   } else {
    //     this.dishes.push(data);
    //   }
    //   this.dishEdit = false;
    // });
    this.dishEdit = false;

    this.uploadForm = this.formBuilder.group({
      file: [''],
    });
    this.newImage = false;
  }

}
