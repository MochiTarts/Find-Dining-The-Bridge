import { Component, OnInit } from '@angular/core';
import { faPlus, faTrash } from '@fortawesome/free-solid-svg-icons';
import { Title } from '@angular/platform-browser';
import { PostService } from 'src/app/_services/post.service';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from '../../_services/token-storage.service';
import { RestaurantService } from '../../_services/restaurant.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';
import { formValidator } from '../../_validation/formValidator';
import { postValidator } from '../../_validation/postValidator';
import { formValidation } from 'src/app/_validation/forms';

@Component({
  selector: 'app-edit-posts',
  templateUrl: './edit-posts.component.html',
  styleUrls: ['./edit-posts.component.scss']
})
export class EditPostsComponent implements OnInit {
  faPlus = faPlus;
  faTrash = faTrash;

  restaurantId: string = '';
  role: string = '';
  email: string = '';
  userId: string = '';
  profileId: string = '';

  posts: any[] = [];
  content: string = '';
  postModalRef: any;
  deleteModalRef: any;
  deletePostId: string = '';
  deletePostIndex: number;

  validator: formValidator = new postValidator();

  constructor(
    private titleService: Title,
    private postService: PostService,
    private authService: AuthService,
    private tokenStorage: TokenStorageService,
    private restaurantService: RestaurantService,
    private postModalService: NgbModal,
    private deleteModalService: NgbModal,
    private router: Router,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Edit Posts | Find Dining Scarborough");

    if (this.authService.isLoggedIn) {
      const user = this.tokenStorage.getUser();
      this.role = user.role;
      this.email = user.email;
      this.userId = user.user_id;
      this.profileId = user.profile_id;
    }

    this.getRestaurantId();
    this.loadPosts();
  }

  /**
   * Retrieves the id of the currently displayed restaurant
   */
  getRestaurantId() {
    this.restaurantService.getPendingRestaurant().subscribe((data) => {
      this.restaurantId = data._id;
    })
  }

  /**
   * Retrieves all the restaurant's posts
   */
  loadPosts() {
    this.postService.getRestaurantPosts().subscribe((data) => {
      this.posts = data.Posts;
    })
  }

  /**
   * Opens the editing modal form for creating a new post
   * @param content - post content
   */
  openPostModal(content) {
    this.content = '';
    this.validator.clearAllErrors();
    this.postModalRef = this.postModalService.open(content, { size: 'lg' });
  }

  /**
   * Opens the delete modal for confirming to delete a post or not
   * 
   * @param content - post content
   * @param id - post id
   * @param index - post index
   */
  openDeleteModal(content, id, index) {
    this.deletePostId = id;
    this.deletePostIndex = index;
    this.deleteModalRef = this.deleteModalService.open(content, { size: 's' });
  }

  /**
   * Performs action to make a new restaurant post
   */
  createPost() {
    if (this.content == '') {
      alert('Please enter your content before posting!');
    } else {
      const postObj = {
        restaurant_id: this.restaurantId,
        content: this.content,
      };

      const post = {
        content: this.content,
        is_profane: this.content,
      }

      this.validator.clearAllErrors();
      let failFlag = this.validator.validateAll(post, (key) => {
        this.validator.setError(key);
      });

      if (!failFlag) {
        this.postService.createPost(postObj).subscribe((data) => {
          if (data && formValidation.isInvalidResponse(data)) {
            formValidation.HandleInvalid(data, (key) => this.validator.setError(key));
            alert("Please ensure the post content is valid");
          } else {
            this.posts.unshift(data);
            this.postModalRef.close();
          }
        });
      } else {
        alert("Please ensure the post content is valid");
      }
    }
  }

  /**
   * Performs action to remove a restaurant post
   */
  deleteContent() {
    this.postService.deletePost(this.deletePostId);

    if (this.deletePostIndex > -1) {
      this.posts.splice(this.deletePostIndex, 1);
    }

    this.deletePostId = '';
    this.deletePostIndex = 0;
    this.deleteModalRef.close();
  }

  back() {
    this.router.navigate(['/restaurant']);
  }

}
