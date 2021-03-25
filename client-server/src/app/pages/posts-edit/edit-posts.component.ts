import { Component, OnInit } from '@angular/core';
import { faPlus, faTrash } from '@fortawesome/free-solid-svg-icons';
import { Title } from '@angular/platform-browser';
import { PostService } from 'src/app/_services/post.service';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from '../../_services/token-storage.service';
import { RestaurantService } from '../../_services/restaurant.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';

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

  getRestaurantId() {
    this.restaurantService.getPendingRestaurant().subscribe((data) => {
      this.restaurantId = data._id;
    })
  }

  loadPosts() {
    this.postService.getRestaurantPosts().subscribe((data) => {
      this.posts = data.Posts;
    })
  }

  openPostModal(content) {
    this.postModalRef = this.postModalService.open(content, { size: 'lg' });
  }

  openDeleteModal(content, id, index) {
    this.deletePostId = id;
    this.deletePostIndex = index;
    this.deleteModalRef = this.deleteModalService.open(content, { size: 's' });
  }

  createPost() {
    if (this.content == '') {
      alert('Please enter your content before posting!');
    } else {
      const postObj = {
        restaurant_id: this.restaurantId,
        content: this.content,
      };

      this.postService.createPost(postObj).subscribe((data) => {
        this.posts.unshift(data);
        this.postModalRef.close();
      });

      this.content = '';
    }
  }

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
