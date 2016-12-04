+++
title = "Customize Gerrit Homepage"
date = "2016-12-03T14:20:37+08:00"
tags        = ["Gerrit"]
categories  = ["Gerrit"]
+++

# Customized Homepage

To customize Gerrit homepage, we added the following files:

* `$site_path/etc/GerritSiteHeader.html` HTML is inserted below the menu bar, but above any page content. This is a good location for an organizational logo.
* `$site_path/etc/GerritSiteFooter.html` HTML is inserted at the bottom of the page, below all other content. Display links to FAQ, user guides, etc.
* `$site_path/etc/GerritSite.css` The customized CSS rules are inlined into the top of the HTML page.
* `$site_path/static/logo.cache.png` The Logo picture.

For more details about how they work, please see [official documents](https://gerrit-review.googlesource.com/Documentation/config-themes.html).


## Examples

* `GerritSiteHeader.html`

```
<div>
  <div id="logo"><a href="#/"><img src="static/logo.cache.png" height="41" width="32"/></a></div>
  <!-- Add more contents if necessary
  <p id="customized_paragraph"><strong>NOTICE</strong></p>
  <ol>
  <li>Maintain/Shutdown Announcements</li>
  <li>New Features</li>
  </ol>
  <p id="customized_paragraph">2016/11/10</p>
  -->
</div>
```

* `GerritSiteFooter.html`

```
<div>
  <ul>
  <li><a href="https://www.mediawiki.org/wiki/Git_and_Gerrit_FAQ" target="_blank">Frequently Asked Questions</a></li>
  <li><a href="https://www.mediawiki.org/wiki/Gerrit/Tutorial" target="_blank">Setup Gerrit</a></li>
  </ul>
  <p id="customized_paragraph">If you have any problem, please contact <a href="mailto:email@example.com" target="_blank">DevOps Team</a></p>
<!-- Add Piwik if necessary -->
</div>
```

* `GerritSite.css`

```
#logo {
  display: block !important;
  margin-bottom: -55px;
  padding-left: 20px;
  position: relative;
  top: -50px;
  width: 60px;
}
#gerrit_topmenu {
  left: 55px;
  margin-right: 55px;
  margin-bottom: 5px;
  position: relative;
}
#customized_paragraph {
  padding-left: 10px;
}
```

# Update Homepage

**NOTICE**: There is no need to restart Gerrit after updating HTML/CSS. The homepage will work immediately after putting HTML/CSS files in $site_path/etc directory.

We use Ansible to deploy Gerrit. Here are examples that how to update HTML/CSS files by Ansible command.


* Adding `GerritSiteHeader.html` to Gerrit

```
ansible production -i hosts [-l <single-gerrit-host>] -m copy -s -a 'src=GerritSiteHeader.html dest=/site_path/etc owner=gerrit2 group=gerrit2 mode=0644' -v
```

* Removing `GerritSiteFooter.html`

```
ansible production -i hosts [-l <single-gerrit-host>] -m file -s -a 'dest=/site_path/etc state=absent' -v
```