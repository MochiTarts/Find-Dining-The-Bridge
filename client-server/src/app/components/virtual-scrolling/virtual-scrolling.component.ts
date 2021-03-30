import { Component, OnInit, ChangeDetectionStrategy, Input } from '@angular/core';
import { PostService } from 'src/app/_services/post.service';
import { BehaviorSubject } from 'rxjs';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-virtual-scrolling',
  templateUrl: './virtual-scrolling.component.html',
  styleUrls: ['./virtual-scrolling.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class VirtualScrollingComponent implements OnInit {
  @Input() restaurantName: string = '';

  restaurantId: string = '';

  posts: any[] = [];
  lstPosts = new BehaviorSubject<any[]>(null);

  constructor(
    private postService: PostService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit(): void {
    this.loadPosts();
  }

  loadPosts() {
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;
    if (this.restaurantId) {
      this.postService.getRestaurantPostsById(this.restaurantId).subscribe((data) => {
        this.posts = data.Posts;
        this.lstPosts.next(this.posts);
      })
    } else {
      this.postService.getRestaurantPosts().subscribe((data) => {
        this.posts = data.Posts;
        this.lstPosts.next(this.posts);
      });
    }

  }

}
