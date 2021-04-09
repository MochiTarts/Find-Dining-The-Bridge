import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleHeadlineCardComponent } from './article-headline-card.component';

describe('ArticleHeadlineCardComponent', () => {
  let component: ArticleHeadlineCardComponent;
  let fixture: ComponentFixture<ArticleHeadlineCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ArticleHeadlineCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArticleHeadlineCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
