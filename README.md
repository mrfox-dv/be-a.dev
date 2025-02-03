<h1 align="center">be-a.dev</h1>

<p align="center"><strong>be-a.dev</strong> is a service that allows developers to get a sweet-looking <code>.be-a.dev</code> domain for their personal websites.</p>

# Register

## How to Register

- Fork this repository
- Add a new file called `your-domain-name.json` in the `domains` folder to register `your-domain-name.be-a.dev`
  - For structure, please refer to [this](/docs/domain-structure.md)
- If you are applying for NS records please read [this](#ns-records).
- Your commit message should be in the format of `Add/Edit/Delete <your-domain-name>.be-a.dev`
- Your pull request will be reviewed and merged. *Make sure to keep an eye on it incase we need you to make any changes!*
- After the pull request is merged, please allow up to 24 hours for the changes to propagate
- Enjoy your new `.be-a.dev` domain! Please consider leaving us a star ⭐️ to help support us!

### NS Records
When applying for NS records, please be aware we already support a [wide range of DNS records](/docs/faq.md#which-records-are-supported), so you may not need them. 

In your PR, please explain why you need NS records, including examples, to help mitigate potential abuse. Refer to the [FAQ](/docs/faq.md#who-can-use-ns-records) for guidelines on allowed usage. 

***Pull requests adding NS records without sufficient reasoning will be closed.***

> Also see: [Why are you so strict with NS records?](/docs/faq.md#why-are-you-so-strict-with-ns-records)

## Report Abuse
If you find any subdomains being used for abusive purposes, please report them by creating an issue with the relevant evidence.

<!--
---

We are proud to announce that we are supported by Cloudflare's [Project Alexandria](https://www.cloudflare.com/lp/project-alexandria) sponsorship program. We would not be able to operate without their help! 💖

<a href="https://www.cloudflare.com">
   <img alt="Cloudflare Logo" src="https://raw.githubusercontent.com/is-a-dev/register/main/media/cloudflare.png" height="96">
</a>
-->
