import { Component, OnInit, Input } from '@angular/core';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';
import { ArticleService } from '../../_services/article.service';

@Component({
  selector: 'app-article-common-card',
  templateUrl: './article-common-card.component.html',
  styleUrls: ['./article-common-card.component.scss']
})
export class ArticleCommonCardComponent implements OnInit {
  @Input() article: any;

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
