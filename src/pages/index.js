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
              All 67 commands and their 41 subcommands, with synopsis, flags and
              examples. The official docs cover 16.
            </p>
          </div>
          <div className="col col--4">
            <Heading as="h3">Real captured output</Heading>
            <p>
              Every example on every page is terminal output captured from a
              live browser, most of it against this site's own fixture so it
              cannot drift. Nothing is transcribed from the binary's{' '}
              <code>--help</code>.
            </p>
          </div>
          <div className="col col--4">
            <Heading as="h3">Regenerable</Heading>
            <p>
              A script reads the installed binary and rebuilds the indexes, the
              global flags page and the command lists, so a new vibium release
              is one command away from being accounted for.
            </p>
          </div>
        </div>
      </main>
    </Layout>
  );
}
