import asyncio
import click

from pyrobot.rgb_leds import RgbUnderlighting, HsvColor


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


@cli.command()
@click.pass_context
@click.option('-h', 'h', default=255, show_default=True)
@click.option('-s', 's', default=255, show_default=True)
@click.option('-v', 'v', default=255, show_default=True)
def all(ctx, h, s, v):
    underligts = ctx.obj['lights']
    underligts.set_color(HsvColor(h, s, v))


@cli.command()
@click.pass_context
@click.option('-h', 'hue', default=0, show_default=True)
@click.option('-s', 'saturation', default=0, show_default=True)
def flash(ctx, hue, saturation):
    underligts = ctx.obj['lights']

    async def main():
        await underligts.flash(hue, saturation)

    asyncio.run(main())


@cli.command()
@click.pass_context
@click.option('-h', 'h', default=255, show_default=True)
@click.option('-s', 's', default=255, show_default=True)
@click.option('-v', 'v', default=255, show_default=True)
@click.argument('pattern')
def set(ctx, h, s, v, pattern):
    underligts = ctx.obj['lights']
    print(pattern)
    underligts.change_color(HsvColor(h, s, v), pattern)


@cli.command()
@click.pass_context
def off(ctx):
    underligts = ctx.obj['lights']
    underligts.turn_off()



if __name__ == '__main__':
    cli(obj={'lights': RgbUnderlighting()})
