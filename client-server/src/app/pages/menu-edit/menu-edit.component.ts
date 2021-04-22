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
import { MediaService } from '../../_services/media.service';

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
  //dishes: any[];
  specialDish: any[] = [];
  popularDish: any[] = [];
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
    private mediaService: MediaService,
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
      //this.dishes = data.Dishes;
      for (let dish of data.Dishes) {
        if (dish.category == "Special") {
          this.specialDish.push(dish);
        } else if (dish.category == "Popular Dish") {
          this.popularDish.push(dish);
        }
      }
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
    this.dishId = dish._id;
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
      var index = this.dishIndex;

      if (this.dishEdit) {
        this.restaurantsService.editPendingDish(dishInfo, this.dishId).subscribe((data) => {
          if (this.newImage) {
            this.onSubmit(data._id, dishInfo.category, index);
          } else {
            if (dishInfo.category == 'Special') {
              this.specialDish[index] = data;
            } else {
              this.popularDish[index] = data;
            }
            this.dishIndex = 0;
            this.dishEdit = false;
          }
        },
        (error) => {
          this.alertMessage = error.error.detail;
          this.showAlert = true;
        });
      } else {
        dishInfo['picture'] = '';
        this.restaurantsService.createPendingDish(dishInfo).subscribe((data) => {
          if (this.newImage) {
            this.onSubmit(data._id, dishInfo.category, index);
          } else {
            if (dishInfo.category == 'Special') {
              this.specialDish.push(data);
            } else {
              this.popularDish.push(data);
            }
          }
        },
        (error) => {
          this.alertMessage = error.error.detail;
          this.showAlert = true;
        });
      }

      this.clearInput();
      this.dishModalRef.close();
    }
  }

  deleteDish() {
    /*var dishInfo = {
      name: this.dishName,
      category: this.menuCategory,
    };*/
    var category = this.menuCategory;
    var index = this.dishIndex;

    this.restaurantsService.deleteDish(this.dishId).subscribe(() => {
      if (category == "Special") {
        if (index > -1) {
          this.specialDish.splice(index, 1);
          console.log(this.specialDish)
        }
      } else {
        if (index > -1) {
          this.popularDish.splice(this.dishIndex, 1);
        }
      }
    });

    /*if (this.dishIndex > -1) {
      this.dishes.splice(this.dishIndex, 1);
    }*/

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

  onSubmit(id: string, category: string, index: number) {
    const formData = new FormData();
    formData.append('media_file', this.uploadForm.get('file').value);
    this.mediaService.uploadDishMedia(formData, id).subscribe((data) => {
      if (this.dishEdit) {
        //this.dishes[this.dishIndex] = data;
        if (category == 'Special') {
          this.specialDish[index] = data;
        } else {
          this.popularDish[index] = data;
        }
        this.dishIndex = 0;
      } else {
        //this.dishes.push(data);
        if (category == 'Special') {
          this.specialDish.push(data);
        } else {
          this.popularDish.push(data);
        }
      }
      this.dishEdit = false;
    });

    this.uploadForm = this.formBuilder.group({
      file: [''],
    });
    this.newImage = false;
  }

}
