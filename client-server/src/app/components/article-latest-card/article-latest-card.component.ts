import { Component, OnInit, Input } from '@angular/core';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';
import { faStar } from '@fortawesome/free-solid-svg-icons';
import { ArticleService } from '../../_services/article.service';

@Component({
  selector: 'app-article-latest-card',
  templateUrl: './article-latest-card.component.html',
  styleUrls: ['./article-latest-card.component.scss']
})
export class ArticleLatestCardComponent implements OnInit {
  @Input() article: any;

  faStar = faStar;

  constructor(
    private userService: UserService,
    private tokenStorage: TokenStorageService,
    private articleService: ArticleService,
  ) { }

  ngOnInit(): void {
  }

  openArticle() {
    this.articleService.openArticle(this.article);
  }

}
