import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link className="button button--secondary button--lg" to="/docs/commands">
            Browse all 67 commands
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  return (
    <Layout
      title="Vibium CLI reference"
      description="An independent, complete command reference for the Vibium browser automation CLI.">
      <HomepageHeader />
      <main className="container margin-vert--lg">
        <div className="row">
          <div className="col col--4">
            <Heading as="h3">Complete</Heading>
            <p>
              All 67 commands and their 37 subcommands, with synopsis, flags and
              examples. The official docs cover 16.
            </p>
          </div>
          <div className="col col--4">
            <Heading as="h3">Honest about its sources</Heading>
            <p>
              Every page says whether its examples are real captured output or
              derived from the binary's <code>--help</code>. No page pretends to
              be more verified than it is.
            </p>
          </div>
          <div className="col col--4">
            <Heading as="h3">Regenerable</Heading>
            <p>
              A script reads the installed binary and rewrites the reference, so
              a new vibium release is one command away from documented.
            </p>
          </div>
        </div>
      </main>
    </Layout>
  );
}
