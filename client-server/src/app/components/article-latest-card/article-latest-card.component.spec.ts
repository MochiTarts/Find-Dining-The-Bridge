import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleLatestCardComponent } from './article-latest-card.component';

describe('ArticleLatestCardComponent', () => {
  let component: ArticleLatestCardComponent;
  let fixture: ComponentFixture<ArticleLatestCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ArticleLatestCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArticleLatestCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
