# Django Model to Gorm Struct

Tool converts django models to Gorm struct

## Usage

Put `djangorm` in INSTALLED_APPS

Then run `python manage.py d2g --apps=<app-name> --lang=go`
Currently supports `go` and `java`

e.g.

sampleproject/sampleapp/models.py

```python
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    description = models.TextField()
    softcopy = models.FileField()
    softcopy_path = models.FilePathField()
    slug = models.SlugField()
    url = models.URLField()
    at_time = models.TimeField()
    uuid = models.UUIDField()

class AuthorProfile(models.Model):
    author = models.OneToOneField(Author, null=True, on_delete=models.SET_NULL)
    color = models.CharField(max_length=10, null=True)


class Book(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, unique=True)
    age = models.PositiveIntegerField(db_index=True)
    birthday = models.DateTimeField()
    member_number = models.CharField(max_length=100,null=True)
    activated_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    title = models.CharField(max_length=255)
    rating = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_good = models.NullBooleanField()
    is_bad = models.BooleanField(default=True)


class Page(models.Model):
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    number = models.IntegerField()
    authors = models.ManyToManyField(Author)
```

Running the command `python manage.py d2g --apps=sampleapp --lang=go`

```go
import (
	"errors"
	"github.com/google/uuid"
	"time"
	"gorm.io/gorm"
)

type Author struct {
    Pages                []*Page                   `gorm:"many2many:sampleapp_page_authors"`
    Id                   uint64                    `gorm:"primaryKey;not null;unique"`
    Name                 string                    `gorm:"type:varchar(100)"`
    Email                string                    `gorm:"type:varchar(254);not null"`
    Description          string                    `gorm:"not null"`
    Softcopy             string                    `gorm:"type:varchar(100);not null"`
    SoftcopyPath         string                    `gorm:"type:varchar(100);not null"`
    Slug                 string                    `gorm:"type:varchar(50);not null;index"`
    Url                  string                    `gorm:"type:varchar(100);not null"`
    AtTime               time.Time                 `gorm:"not null"`
    Uuid                 uuid.UUID                 `gorm:"type:uuid;default:uuid_generate_v4();not null"`
}

func(Author) TableName() string {
    return "sampleapp_author"
}

type AuthorProfile struct {
    Id                   uint64                    `gorm:"primaryKey;not null;unique"`
    AuthorId             uint32                    `gorm:"index;unique"`
    Author               Author                    `gorm:"foreignKey:AuthorId;constraint:OnDelete:SET NULL;index;unique"`
    Color                string                    `gorm:"type:varchar(10)"`
}

func(AuthorProfile) TableName() string {
    return "sampleapp_authorprofile"
}

type Book struct {
    Id                   uint64                    `gorm:"primaryKey;not null;unique"`
    Name                 string                    `gorm:"type:varchar(100)"`
    Email                string                    `gorm:"type:varchar(100);not null;unique"`
    Age                  uint32                    `gorm:"check:age>0;not null;index"`
    Birthday             time.Time                 `gorm:"not null"`
    MemberNumber         string                    `gorm:"type:varchar(100)"`
    ActivatedAt          time.Time
    CreatedAt            time.Time                 `gorm:"not null"`
    UpdatedAt            time.Time                 `gorm:"not null"`
    Title                string                    `gorm:"type:varchar(255);not null"`
    Rating               int32                     `gorm:"not null"`
    AuthorId             uint32                    `gorm:"index"`
    Author               Author                    `gorm:"foreignKey:AuthorId;constraint:OnDelete:CASCADE;not null;index"`
    IsGood               bool
    IsBad                bool                      `gorm:"not null"`
}

func(Book) TableName() string {
    return "sampleapp_book"
}

type Page struct {
    Id                   uint64                    `gorm:"primaryKey;not null;unique"`
    BookId               uint32                    `gorm:"index"`
    Book                 Book                      `gorm:"foreignKey:BookId;constraint:OnDelete:SET NULL;index"`
    Number               int32                     `gorm:"not null"`
    Authors              []*Author                 `gorm:"many2many:sampleapp_page_authors;not null"`
}

func(Page) TableName() string {
    return "sampleapp_page"
}
```
