# Glossary

Every term the entries use, explained from zero with an everyday comparison. Each comparison is a way in, not a definition; where it breaks, the entry says so.

## Bittensor

A network of small, independent marketplaces for digital work, sharing one currency. Think of a trade fair with a hundred booths: each booth runs its own competition, pays its own winners, and sells its own product, but every booth is paid out of one shared prize fund and every ticket is bought with the same money. The fund is TAO, the booths are subnets, and the rule for splitting the fund is written in code rather than decided by a manager.

## TAO

The network's money. It is created at a steady rate, like a mint that prints a fixed number of coins per day, and handed out to the subnets that the market values most. Anyone can buy TAO on an exchange; anyone holding it can stake it into a subnet to earn that subnet's token.

## Subnet

One booth at the trade fair: a marketplace for a single kind of digital work, with its own rules, its own workers, its own judges, and its own token. Each subnet has a number (SN64 is the sixty-fourth). A subnet is not a company; it is a set of rules that a company, a foundation, or a single developer can publish and that strangers then compete inside.

## Digital commodity

The thing a subnet produces and sells, as interchangeable as wheat or electricity: an hour of GPU time, a million words of model output, a trained model checkpoint, a forecast, a verified dataset. The word "commodity" is the point. A subnet that cannot say what its unit of output is has not decided what it sells.

## Miner

A worker who does the subnet's task and gets paid by how well they do it. Like a freelancer on a gig platform, except the platform is code, the jobs arrive automatically, and pay is decided by the judges' scores rather than by a client. A miner might be a person with a laptop or a company with a warehouse of GPUs; the network cannot tell and does not care.

## Validator

A judge who sends work to miners, scores the results, and by scoring decides who gets paid. Like a restaurant critic whose reviews directly set each kitchen's wages. Validators have to put up money (a stake) to hold the role, and their scores are weighted by how much money stands behind them.

## Emission

The subnet's share of the newly minted TAO, paid out block by block to its miners, validators, and owner. Like the prize fund at the trade fair being divided among the booths every few seconds. Since June 2026 a subnet's share follows the price of its token, so the market, not a committee, decides which booths are worth funding.

## Alpha token

Each subnet's own token, created when someone stakes TAO into that subnet. Staking is a swap: TAO goes into the subnet's pool and the staker gets alpha out, like exchanging dollars for casino chips that only work at one table. The alpha's price rises when more TAO flows in and falls when it flows out, and that price is what sets the subnet's emission share.

## Staking

Locking TAO into a subnet to receive its alpha token and a share of its rewards. Like putting money into one booth's till and owning a slice of that booth's takings. Unstaking swaps the alpha back to TAO at whatever the price is then.

## dTAO

The rule change, in February 2025, that gave every subnet its own token and let the market set emission instead of a vote. Before dTAO, a small group of large validators decided which subnets deserved rewards. After it, whoever stakes decides, with their money. Every entry on this site assumes the dTAO world.

## Incentive mechanism

The subnet's rulebook: what task the miners do, how the validators score it, and how the score turns into pay. Like the scoring rules of a sport. Two subnets can sell the same commodity with very different mechanisms, and the mechanism is where most of the cleverness, and most of the cheating, lives.

## Deregistration

Losing your slot in a subnet because your score fell to the bottom. Each subnet has a fixed number of seats; when a new miner registers, the lowest-scoring one is dropped. Like a league with relegation every round. New entrants usually get a short immunity period before they can be dropped.

## Registration cost

The fee, paid in TAO, to take a seat as a miner or validator in a subnet. It is burned, not paid to anyone, and it rises when lots of people are trying to get in. Like an entry fee that goes up with the queue.

## Inference

Asking a trained AI model a question and getting an answer. The model is not learning; it is being used. Inference is the most common commodity on Bittensor because it is easy to meter: one request in, one response out, a price per million words.

## Checkpoint

A saved copy of a trained model's weights at a moment in time, the file you would download to run the model yourself. Like a snapshot of a student's knowledge that anyone can copy. Subnets that train models produce checkpoints as their commodity.

## Training

Teaching a model by feeding it data and adjusting it, the expensive process that produces a checkpoint. Some subnets pay miners to do pieces of training on their own hardware and stitch the results together, which is the hard technical bet Bittensor is known for.

## TEE

Trusted execution environment: a locked box inside a computer's processor that can prove what code ran inside it and that nobody, including the machine's owner, tampered with it. Like a tamper-evident seal on a ballot box. Subnets use TEEs so validators can trust a miner's work without redoing it.

## GPU

The graphics processor that does most AI computing, sold by the hour like a rental car. When an entry says "compute," it almost always means GPU hours.

## Netuid

A subnet's number on the chain. SN107 means netuid 107. Numbers are permanent; names and owners can change, which is why every page here is keyed by number.
