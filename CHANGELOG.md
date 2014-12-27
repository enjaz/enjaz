Change Log
==========
Changes are ordered latest-first.

### 27 Dec 2014 (Saeed)
* Deprecated `get_approved_activities()`, `get_pending_activities()`, and `get_rejected_activities()`. These
  are now replaced by the manager methods `approved()`, `pending()`, and `rejected()`, respectively, so that
  calling `Activity.objects.approved()` is the same as previously calling `get_approved_activities()` and so on.
* Introduced custom template filters for checking permissions in templates.
  I've written the details [here](https://github.com/osamak/student-portal/issues/32#issuecomment-68181435).
 
### 27 Dec 2014
* First Entry. No changes have been logged prior to this point.
